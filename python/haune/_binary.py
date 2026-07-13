"""Resolve (and, if needed, auto-download) the HauneBrowser stealth binary.

Resolution order:
  1. ``executable_path`` passed to :func:`haune.launch`
  2. ``$HAUNE_CHROME`` environment variable
  3. a previously cached download under ``~/.haune/bin/<tag>/``
  4. download + extract the release archive from GitHub (``$HAUNE_BROWSER_URL`` overrides)

The binary is distributed as a self-contained release archive; no source is shipped.
"""
from __future__ import annotations

import hashlib
import os
import zipfile
from pathlib import Path

import requests

# The published release archive. Override with $HAUNE_BROWSER_URL for a private mirror.
RELEASE_TAG = os.environ.get("HAUNE_BROWSER_TAG", "v1.0.0")
DEFAULT_URL = os.environ.get(
    "HAUNE_BROWSER_URL",
    f"https://github.com/haune2311/haune-antidetect/releases/download/{RELEASE_TAG}/HauneBrowser-win-x64.zip",
)
# SHA-256 of the release archive — verified before extraction so a tampered/compromised
# mirror is rejected. Override with $HAUNE_BROWSER_SHA256 when pinning a different build.
EXPECTED_SHA256 = os.environ.get(
    "HAUNE_BROWSER_SHA256",
    "1215f9005e703dbe01690d28b46f1d08a6572de5f1375b13a1b259905db9adcc",
)

_CACHE = Path.home() / ".haune" / "bin" / RELEASE_TAG
_EXE_NAME = "chrome.exe"


def _find_exe(root: Path) -> Path | None:
    if not root.exists():
        return None
    direct = root / _EXE_NAME
    if direct.exists():
        return direct
    for p in root.rglob(_EXE_NAME):
        return p
    return None


def _download_and_extract() -> Path:
    _CACHE.mkdir(parents=True, exist_ok=True)
    archive = _CACHE / "HauneBrowser.zip"
    if not archive.exists():
        print(f"[haune] downloading browser binary ({DEFAULT_URL}) ...")
        with requests.get(DEFAULT_URL, stream=True, timeout=120) as r:
            r.raise_for_status()
            h = hashlib.sha256()
            with open(archive, "wb") as f:
                for chunk in r.iter_content(chunk_size=1 << 20):
                    f.write(chunk)
                    h.update(chunk)
        if EXPECTED_SHA256 and h.hexdigest().lower() != EXPECTED_SHA256.lower():
            archive.unlink(missing_ok=True)
            raise RuntimeError("Haune binary checksum mismatch — download rejected.")
    with zipfile.ZipFile(archive) as z:
        z.extractall(_CACHE)
    exe = _find_exe(_CACHE)
    if not exe:
        raise RuntimeError("Haune binary archive did not contain chrome.exe")
    return exe


def resolve_executable(executable_path: str | None = None) -> str:
    if executable_path:
        return executable_path
    env = os.environ.get("HAUNE_CHROME")
    if env and Path(env).exists():
        return env
    cached = _find_exe(_CACHE)
    if cached:
        return str(cached)
    return str(_download_and_extract())
