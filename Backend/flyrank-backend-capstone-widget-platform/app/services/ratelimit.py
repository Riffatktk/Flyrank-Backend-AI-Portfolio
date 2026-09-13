"""
In-memory fixed-window rate limiter (per IP, per widget).

Free-tool scope for this capstone: no Redis dependency required. It's a
single-process limiter -- fine for a capstone; swap for Redis (INCR + EXPIRE)
if you deploy across multiple workers.
"""
import time
from collections import defaultdict

from app.config import settings

# key -> list of unix timestamps of recent hits
_hits: dict[str, list[float]] = defaultdict(list)

WINDOW_SECONDS = 60


def _key(ip: str, widget_id: str) -> str:
    return f"{ip}:{widget_id}"


def is_rate_limited(ip: str, widget_id: str) -> bool:
    now = time.time()
    k = _key(ip, widget_id)

    # drop hits older than the window
    _hits[k] = [t for t in _hits[k] if now - t < WINDOW_SECONDS]

    if len(_hits[k]) >= settings.rate_limit_per_minute:
        return True

    _hits[k].append(now)
    return False
