# Haune (Python)

Anti-detect browser for Python — a drop-in [Playwright](https://playwright.dev/python/)
launcher that drives the **HauneBrowser** stealth binary. Fingerprints are handled inside
the browser core (source-level, compiled in), so detection systems see a real browser.

The binary auto-downloads on first run (self-contained, cached under `~/.haune`); no source
is shipped.

## Install

```bash
pip install haune
```

## Use

```python
from haune import launch

# Clean by default. With a proxy, timezone / geolocation / WebRTC IP auto-match the exit.
browser = launch(proxy="http://user:pass@host:port", headless=False)
page = browser.new_page()
page.goto("https://example.com")
print(page.title())
browser.close()
```

Persistent profile (cookies/localStorage survive across runs):

```python
from haune import launch_persistent_context

ctx = launch_persistent_context("./profile", seed=12345, proxy="socks5://user:pass@host:port")
page = ctx.new_page()
page.goto("https://example.com")
ctx.close()
```

## `launch()` options

| Option | Default | Meaning |
|---|---|---|
| `seed` | random | Identity seed — same seed reproduces the same device. |
| `proxy` | `None` | `http(s)://` or `socks5://`, with embedded `user:pass@`. |
| `headless` | `True` | Headful recommended for the hardest sites. |
| `geoip` | `True` | Match timezone / geolocation / WebRTC IP to the proxy exit. |
| `spoof_gpu` | `False` | Also spoof the GPU renderer string (kept real by default). |
| `timezone` | auto | Override the timezone (IANA name). |
| `executable_path` | auto | Use a specific binary instead of the auto-download. |

Set `HAUNE_CHROME` to point at an existing binary, or `HAUNE_BROWSER_URL` for a private
download mirror.

## License

Proprietary — © Haune. All rights reserved. See the project LICENSE.
Windows x64.
