using System.Globalization;
using Microsoft.Playwright;

namespace Haune;

/// <summary>
/// Entry point for HauneBrowser — an anti-detect browser for .NET. Drives the HauneBrowser
/// stealth binary (auto-downloaded on first run) with the clean-default config: seed +
/// geo/timezone coherence, GPU kept real, canvas farbled per-seed by the binary. No
/// fingerprint generator lives here — it is compiled into the binary.
/// </summary>
public static class HauneLauncher
{
    private const string DisBase = "canvas,webgl,gpu,audio,font,clientrects";
    private const string DisGpu = "canvas,webgl,audio,font,clientrects"; // gpu excluded => renderer spoofed

    /// <summary>Launch a HauneBrowser as a synthesized identity.</summary>
    public static async Task<HauneBrowser> LaunchAsync(LaunchOptions? options = null)
    {
        options ??= new LaunchOptions();

        var exe = await BinaryManager.ResolveAsync(options.ExecutablePath);
        var proxy = string.IsNullOrEmpty(options.Proxy) ? null : ProxyInfo.Parse(options.Proxy!);
        var wantGeoIp = options.GeoIp ?? (proxy is not null);

        ExitInfo? exit = null;
        if (proxy is not null && wantGeoIp)
            exit = await GeoIp.ResolveAsync(proxy);

        var seed = options.Seed ?? Random.Shared.NextInt64(1, long.MaxValue);
        var tz = options.Timezone ?? exit?.Timezone;

        var args = new List<string>
        {
            "--no-first-run",
            "--no-default-browser-check",
            $"--fingerprint={seed}",
            $"--disable-spoofing={(options.SpoofGpu ? DisGpu : DisBase)}",
        };
        if (!string.IsNullOrEmpty(tz)) args.Add($"--timezone={tz}");
        if (exit?.Ip is not null) args.Add($"--fingerprint-webrtc-ip={exit.Ip}");
        if (exit is { Lat: { } la, Lon: { } lo })
            args.Add($"--fingerprint-location={la.ToString(CultureInfo.InvariantCulture)},{lo.ToString(CultureInfo.InvariantCulture)}");
        args.AddRange(options.Args);

        var pw = await Playwright.CreateAsync();
        var launch = new BrowserTypeLaunchOptions { ExecutablePath = exe, Headless = options.Headless, Args = args };
        if (proxy is not null)
            launch.Proxy = new Proxy { Server = proxy.Server, Username = proxy.Username, Password = proxy.Password };

        var browser = await pw.Chromium.LaunchAsync(launch);
        return new HauneBrowser(pw, browser, seed);
    }
}
