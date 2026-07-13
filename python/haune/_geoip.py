"""Resolve a proxy's exit country / timezone / lat-lon / IP so the identity's geo
signals (timezone, geolocation, WebRTC IP) can be made coherent with the exit — the
same ``geoip=True`` behaviour users expect from an anti-detect browser."""
from __future__ import annotations

from dataclasses import dataclass

import requests


@dataclass
class ExitInfo:
    ip: str | None = None
    country: str | None = None
    timezone: str | None = None
    lat: float | None = None
    lon: float | None = None


def resolve_exit(proxy: str | None) -> ExitInfo | None:
    """One round-trip through the proxy to ip-api.com (free, no token)."""
    if not proxy:
        return None
    try:
        proxies = {"http": proxy, "https": proxy}
        r = requests.get(
            "http://ip-api.com/json?fields=status,countryCode,timezone,lat,lon,query",
            proxies=proxies,
            timeout=15,
        )
        j = r.json()
        if j.get("status") != "success":
            return None
        return ExitInfo(
            ip=j.get("query"),
            country=j.get("countryCode"),
            timezone=j.get("timezone"),
            lat=j.get("lat"),
            lon=j.get("lon"),
        )
    except Exception:
        return None
