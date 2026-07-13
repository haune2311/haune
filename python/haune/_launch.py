"""Build the launch flags for the HauneBrowser binary.

Default = the cleanest config: seed + timezone + disable-spoofing (readback noise off,
GPU kept real / native passthrough), canvas farbled per-seed by the binary's native
render layer. ``spoof_gpu=True`` also spoofs the GPU renderer string. Geo signals
(timezone, geolocation, WebRTC IP) are pinned to the proxy exit when a proxy is set.
"""
from __future__ import annotations

import random

from ._geoip import ExitInfo

_DIS_BASE = "canvas,webgl,gpu,audio,font,clientrects"
_DIS_GPU = "canvas,webgl,audio,font,clientrects"  # gpu excluded => renderer spoofed


def build_args(
    seed: int | None,
    exit_info: ExitInfo | None,
    spoof_gpu: bool = False,
    timezone: str | None = None,
    extra_args: list[str] | None = None,
) -> tuple[int, list[str]]:
    if seed is None:
        seed = random.randint(1, 2**53 - 1)

    tz = timezone or (exit_info.timezone if exit_info else None)

    args = [
        "--no-first-run",
        "--no-default-browser-check",
        f"--fingerprint={seed}",
        f"--disable-spoofing={_DIS_GPU if spoof_gpu else _DIS_BASE}",
    ]
    if tz:
        args.append(f"--timezone={tz}")

    if exit_info and exit_info.ip:
        args.append(f"--fingerprint-webrtc-ip={exit_info.ip}")
    if exit_info and exit_info.lat is not None and exit_info.lon is not None:
        args.append(f"--fingerprint-location={exit_info.lat},{exit_info.lon}")

    if extra_args:
        args.extend(extra_args)
    return seed, args
