"""Haune — anti-detect browser (Python).

Drop-in Playwright launcher that drives the HauneBrowser stealth binary. The binary
(with all fingerprint defenses compiled in) auto-downloads on first run; no source is
shipped. Three lines to unblock:

    from haune import launch

    browser = launch(proxy="http://user:pass@host:port")
    page = browser.new_page()
    page.goto("https://example.com")
    browser.close()

Every ``seed`` reproduces the same device. With a proxy, timezone / geolocation / WebRTC
IP auto-match the exit (``geoip=True`` by default). ``spoof_gpu=True`` also spoofs the GPU
string; ``humanize`` / behavioral helpers ship in the binary.
"""
from __future__ import annotations

from playwright.sync_api import sync_playwright

from ._binary import resolve_executable
from ._geoip import resolve_exit
from ._launch import build_args

__version__ = "1.0.0"
__all__ = ["launch", "launch_persistent_context", "HauneBrowser", "HauneContext"]


def _proxy_dict(proxy: str | None):
    if not proxy:
        return None
    # playwright wants {server, username, password}; split embedded creds if present.
    from urllib.parse import urlparse

    u = urlparse(proxy if "://" in proxy else "http://" + proxy)
    d = {"server": f"{u.scheme}://{u.hostname}:{u.port}" if u.port else f"{u.scheme}://{u.hostname}"}
    if u.username:
        d["username"] = u.username
    if u.password:
        d["password"] = u.password
    return d


class HauneBrowser:
    """Thin handle over a Playwright Browser driving the Haune binary."""

    def __init__(self, pw, browser, seed: int):
        self._pw = pw
        self.browser = browser
        self.seed = seed

    def new_page(self, **kw):
        return self.browser.new_page(**kw)

    def new_context(self, **kw):
        return self.browser.new_context(**kw)

    def close(self):
        try:
            self.browser.close()
        finally:
            self._pw.stop()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


class HauneContext:
    """Thin handle over a persistent BrowserContext driving the Haune binary."""

    def __init__(self, pw, context, seed: int):
        self._pw = pw
        self.context = context
        self.seed = seed

    def new_page(self, **kw):
        return self.context.new_page(**kw)

    def close(self):
        try:
            self.context.close()
        finally:
            self._pw.stop()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def _prepare(seed, proxy, geoip, spoof_gpu, timezone, executable_path, args):
    exe = resolve_executable(executable_path)
    exit_info = resolve_exit(proxy) if (proxy and geoip) else None
    seed, launch_args = build_args(seed, exit_info, spoof_gpu, timezone, args)
    return exe, _proxy_dict(proxy), seed, launch_args


def launch(
    seed: int | None = None,
    proxy: str | None = None,
    headless: bool = True,
    geoip: bool = True,
    spoof_gpu: bool = False,
    timezone: str | None = None,
    executable_path: str | None = None,
    args: list[str] | None = None,
) -> HauneBrowser:
    """Launch a Haune browser. Returns a :class:`HauneBrowser` (call ``.new_page()``)."""
    exe, proxy_d, seed, launch_args = _prepare(
        seed, proxy, geoip, spoof_gpu, timezone, executable_path, args
    )
    pw = sync_playwright().start()
    browser = pw.chromium.launch(
        executable_path=exe, headless=headless, proxy=proxy_d, args=launch_args
    )
    return HauneBrowser(pw, browser, seed)


def launch_persistent_context(
    user_data_dir: str,
    seed: int | None = None,
    proxy: str | None = None,
    headless: bool = True,
    geoip: bool = True,
    spoof_gpu: bool = False,
    timezone: str | None = None,
    executable_path: str | None = None,
    args: list[str] | None = None,
) -> HauneContext:
    """Launch a persistent context (cookies/localStorage survive) as a Haune identity."""
    exe, proxy_d, seed, launch_args = _prepare(
        seed, proxy, geoip, spoof_gpu, timezone, executable_path, args
    )
    pw = sync_playwright().start()
    context = pw.chromium.launch_persistent_context(
        user_data_dir,
        executable_path=exe,
        headless=headless,
        proxy=proxy_d,
        args=launch_args,
    )
    return HauneContext(pw, context, seed)
