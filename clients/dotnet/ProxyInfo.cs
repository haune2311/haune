namespace Haune;

/// <summary>A proxy parsed into Playwright's {server, username, password} shape.</summary>
public sealed record ProxyInfo(string Server, string? Username, string? Password)
{
    /// <summary>Parse "scheme://user:pass@host:port" or "host:port" (defaults to http://).</summary>
    public static ProxyInfo Parse(string proxy)
    {
        var u = new Uri(proxy.Contains("://") ? proxy : "http://" + proxy);
        var server = u.IsDefaultPort ? $"{u.Scheme}://{u.Host}" : $"{u.Scheme}://{u.Host}:{u.Port}";
        string? user = null, pass = null;
        if (!string.IsNullOrEmpty(u.UserInfo))
        {
            var parts = u.UserInfo.Split(':', 2);
            user = Uri.UnescapeDataString(parts[0]);
            if (parts.Length > 1) pass = Uri.UnescapeDataString(parts[1]);
        }
        return new ProxyInfo(server, user, pass);
    }
}
