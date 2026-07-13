using Microsoft.Playwright;

namespace Haune;

/// <summary>A launched HauneBrowser. Dispose to close the browser and the driver.</summary>
public sealed class HauneBrowser : IAsyncDisposable
{
    private readonly IPlaywright _pw;

    internal HauneBrowser(IPlaywright pw, IBrowser browser, long seed)
    {
        _pw = pw;
        RawBrowser = browser;
        Seed = seed;
    }

    /// <summary>The seed of the presented identity.</summary>
    public long Seed { get; }

    /// <summary>The underlying Playwright browser (full API available).</summary>
    public IBrowser RawBrowser { get; }

    public Task<IPage> NewPageAsync() => RawBrowser.NewPageAsync();

    public Task<IBrowserContext> NewContextAsync(BrowserNewContextOptions? options = null)
        => RawBrowser.NewContextAsync(options);

    public async ValueTask DisposeAsync()
    {
        await RawBrowser.CloseAsync();
        _pw.Dispose();
    }
}
