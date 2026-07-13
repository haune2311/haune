# Haune (.NET)

Anti-detect browser for .NET — a drop-in launcher (on Microsoft.Playwright) that drives the
**HauneBrowser** stealth binary. Fingerprints are handled inside the browser core, so
detection systems see a real browser. The binary auto-downloads on first run (cached under
`~/.haune`); no source is shipped.

```bash
dotnet add package Haune
```

```csharp
using Haune;

await using var browser = await HauneLauncher.LaunchAsync(new LaunchOptions {
    Proxy    = "http://user:pass@host:port",  // GeoIP + WebRTC auto-enable with a proxy
    Headless = false,
});
var page = await browser.NewPageAsync();
await page.GotoAsync("https://example.com");
```

Every `Seed` reproduces the same device. With a proxy, timezone / geolocation / WebRTC IP
auto-match the exit. `SpoofGpu = true` also spoofs the GPU string (kept real by default).

Proprietary — © Haune. All rights reserved. Windows x64.
