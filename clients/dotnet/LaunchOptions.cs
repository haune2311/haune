namespace Haune;

/// <summary>Options for launching HauneBrowser.</summary>
public sealed class LaunchOptions
{
    /// <summary>Identity seed. Same seed reproduces the same device. Null = random.</summary>
    public long? Seed { get; set; }

    /// <summary>Proxy: "scheme://user:pass@host:port" or "host:port". Null = direct.</summary>
    public string? Proxy { get; set; }

    /// <summary>Run without a visible window. Default true.</summary>
    public bool Headless { get; set; } = true;

    /// <summary>Match timezone / geolocation / WebRTC IP to the proxy exit. Null = on when a proxy is set.</summary>
    public bool? GeoIp { get; set; }

    /// <summary>Also spoof the GPU renderer string (kept real by default).</summary>
    public bool SpoofGpu { get; set; }

    /// <summary>Override the timezone (IANA name). Null = auto (proxy exit).</summary>
    public string? Timezone { get; set; }

    /// <summary>Use a specific binary instead of the auto-download.</summary>
    public string? ExecutablePath { get; set; }

    /// <summary>Extra raw browser flags appended after the defaults.</summary>
    public List<string> Args { get; set; } = new();
}
