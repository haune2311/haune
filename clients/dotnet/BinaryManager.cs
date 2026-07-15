using System.IO.Compression;
using System.Security.Cryptography;

namespace Haune;

/// <summary>Resolves (and, if needed, downloads) the HauneBrowser stealth binary.
/// Order: explicit path → $HAUNE_CHROME → cached download → download the release archive.
/// The binary is a self-contained release archive; no source is shipped.</summary>
public static class BinaryManager
{
    private const string ReleaseTag = "v2.0.0";
    private static readonly string Url =
        Environment.GetEnvironmentVariable("HAUNE_BROWSER_URL")
        ?? $"https://github.com/haune2311/haune-antidetect/releases/download/{ReleaseTag}/HauneBrowser-win-x64.zip";
    private static readonly string ExpectedSha256 =
        Environment.GetEnvironmentVariable("HAUNE_BROWSER_SHA256")
        ?? "401c67c5df3036f1b7c953be322fee951f30d4efa8184166261b9aa38d392c71";

    private static string CacheDir =>
        Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".haune", "bin", ReleaseTag);

    private static string? FindExe(string root)
    {
        if (!Directory.Exists(root)) return null;
        var direct = Path.Combine(root, "chrome.exe");
        if (File.Exists(direct)) return direct;
        return Directory.EnumerateFiles(root, "chrome.exe", SearchOption.AllDirectories).FirstOrDefault();
    }

    public static async Task<string> ResolveAsync(string? executablePath = null)
    {
        if (!string.IsNullOrEmpty(executablePath)) return executablePath!;
        var env = Environment.GetEnvironmentVariable("HAUNE_CHROME");
        if (!string.IsNullOrEmpty(env) && File.Exists(env)) return env!;
        var cached = FindExe(CacheDir);
        if (cached != null) return cached;
        return await DownloadAsync();
    }

    private static async Task<string> DownloadAsync()
    {
        Directory.CreateDirectory(CacheDir);
        var archive = Path.Combine(CacheDir, "HauneBrowser.zip");
        if (!File.Exists(archive))
        {
            Console.WriteLine($"[haune] downloading browser binary ({Url}) ...");
            using var http = new HttpClient { Timeout = TimeSpan.FromMinutes(10) };
            await using (var src = await http.GetStreamAsync(Url))
            await using (var dst = File.Create(archive))
                await src.CopyToAsync(dst);

            await using (var f = File.OpenRead(archive))
            {
                var hash = Convert.ToHexString(await SHA256.HashDataAsync(f)).ToLowerInvariant();
                if (!string.Equals(hash, ExpectedSha256, StringComparison.OrdinalIgnoreCase))
                {
                    File.Delete(archive);
                    throw new InvalidOperationException("Haune binary checksum mismatch — download rejected.");
                }
            }
        }
        ZipFile.ExtractToDirectory(archive, CacheDir, overwriteFiles: true);
        return FindExe(CacheDir) ?? throw new InvalidOperationException("Haune archive did not contain chrome.exe");
    }
}
