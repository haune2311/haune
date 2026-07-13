using System.Net;
using System.Text.Json;

namespace Haune;

/// <summary>The public IP / country / timezone / lat-lon seen at a proxy's exit, so the
/// identity's geo signals can be made coherent with it (geoip=true behaviour).</summary>
public sealed record ExitInfo(string? Ip, string? Country, string? Timezone, double? Lat, double? Lon);

public static class GeoIp
{
    /// <summary>One round-trip through the proxy to ip-api.com (free, no token).</summary>
    public static async Task<ExitInfo?> ResolveAsync(ProxyInfo proxy, CancellationToken ct = default)
    {
        try
        {
            var handler = new HttpClientHandler
            {
                UseProxy = true,
                Proxy = new WebProxy(proxy.Server)
                {
                    Credentials = proxy.Username is null
                        ? null
                        : new NetworkCredential(proxy.Username, proxy.Password),
                },
            };
            using var http = new HttpClient(handler) { Timeout = TimeSpan.FromSeconds(15) };
            var json = await http.GetStringAsync(
                "http://ip-api.com/json?fields=status,countryCode,timezone,lat,lon,query", ct);
            using var doc = JsonDocument.Parse(json);
            var root = doc.RootElement;
            if (root.TryGetProperty("status", out var st) && st.GetString() != "success")
                return null;
            return new ExitInfo(
                root.TryGetProperty("query", out var q) ? q.GetString() : null,
                root.TryGetProperty("countryCode", out var c) ? c.GetString() : null,
                root.TryGetProperty("timezone", out var t) ? t.GetString() : null,
                root.TryGetProperty("lat", out var la) && la.ValueKind == JsonValueKind.Number ? la.GetDouble() : null,
                root.TryGetProperty("lon", out var lo) && lo.ValueKind == JsonValueKind.Number ? lo.GetDouble() : null);
        }
        catch
        {
            return null;
        }
    }
}
