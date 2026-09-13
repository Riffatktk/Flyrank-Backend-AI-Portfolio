"""
IP -> geolocation enrichment with a provider fallback chain.

Provider A: ip-api.com   (free, no key, 45 req/min)
Provider B: ipapi.co     (free tier, ~1000 lookups/day, no key)

If A fails/is toggled down, try B. If both fail, return None -- the caller
MUST still store the submission without geo data. Enrichment must never be
allowed to fail the request.
"""
import httpx

from app.config import settings

PROVIDER_A_URL = "http://ip-api.com/json/{ip}"
PROVIDER_B_URL = "https://ipapi.co/{ip}/json/"


def _query_provider_a(ip: str) -> dict | None:
    if settings.geo_provider_a_down:
        return None
    try:
        resp = httpx.get(PROVIDER_A_URL.format(ip=ip), timeout=3)
        resp.raise_for_status()
        payload = resp.json()
        if payload.get("status") != "success":
            return None
        return {
            "country": payload.get("country"),
            "city": payload.get("city"),
            "provider": "ip-api.com",
        }
    except Exception:
        return None


def _query_provider_b(ip: str) -> dict | None:
    if settings.geo_provider_b_down:
        return None
    try:
        resp = httpx.get(PROVIDER_B_URL.format(ip=ip), timeout=3)
        resp.raise_for_status()
        payload = resp.json()
        if payload.get("error"):
            return None
        return {
            "country": payload.get("country_name"),
            "city": payload.get("city"),
            "provider": "ipapi.co",
        }
    except Exception:
        return None


def enrich_ip(ip: str) -> dict | None:
    """Returns {country, city, provider} or None if every provider failed."""
    # Skip enrichment for local/loopback IPs during local dev/testing
    if ip in ("127.0.0.1", "testclient", "::1") or ip.startswith("192.168.") or ip.startswith("10."):
        return None

    result = _query_provider_a(ip)
    if result:
        return result

    result = _query_provider_b(ip)
    if result:
        return result

    return None
