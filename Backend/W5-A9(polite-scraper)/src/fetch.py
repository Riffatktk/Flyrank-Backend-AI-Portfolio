"""Stage 1 & Stage 5: fetch a URL politely, cache it, and never crash the run.

A page is only ever fetched from the real site once. Every re-run during
development reads the saved copy in cache/. Failures are handled per-page so
one broken URL cannot take the whole run down.
"""
import os
import time
import hashlib
import requests

from . import config


class FetchResult:
    def __init__(self, url, html, status_code, from_cache, error=None):
        self.url = url
        self.html = html
        self.status_code = status_code
        self.from_cache = from_cache
        self.error = error  # short human reason, or None

    @property
    def ok(self):
        return self.html is not None and self.error is None


class Fetcher:
    """Tracks stats across a run: pages fetched for real, cache hits, failures."""

    def __init__(self, cache_dir=config.CACHE_DIR):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": config.USER_AGENT})

        self.pages_fetched = 0   # real network requests that succeeded
        self.cache_hits = 0
        self.failed_pages = []   # list of {"url":..., "reason":...}

    def _cache_path(self, url):
        # Stable, readable-ish filename per URL.
        digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
        safe_tail = url.rstrip("/").split("/")[-1][:40] or "page"
        return os.path.join(self.cache_dir, f"{safe_tail}-{digest}.html")

    def fetch(self, url, label=None):
        """Return a FetchResult. Reads cache if present; otherwise fetches
        politely, retries once on timeout/5xx, and never retries 403/404."""
        cache_path = self._cache_path(url)

        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                html = f.read()
            self.cache_hits += 1
            print(f"CACHE HIT  {label or url}  ({len(html)} bytes)")
            return FetchResult(url, html, 200, from_cache=True)

        attempt = 0
        max_attempts = 2  # one real try + one retry, only for timeout/5xx
        while attempt < max_attempts:
            attempt += 1
            try:
                resp = self.session.get(url, timeout=config.REQUEST_TIMEOUT_SECONDS)
            except requests.exceptions.Timeout:
                if attempt < max_attempts:
                    time.sleep(config.RETRY_WAIT_SECONDS)
                    continue
                reason = "timeout after retry"
                self.failed_pages.append({"url": url, "reason": reason})
                return FetchResult(url, None, None, from_cache=False, error=reason)
            except requests.exceptions.RequestException as exc:
                reason = f"request error: {exc}"
                self.failed_pages.append({"url": url, "reason": reason})
                return FetchResult(url, None, None, from_cache=False, error=reason)

            if resp.status_code == 200:
                html = resp.content.decode("utf-8", errors="replace")
                with open(cache_path, "w", encoding="utf-8") as f:
                    f.write(html)
                self.pages_fetched += 1
                print(f"FETCH      {label or url}  status=200  ({len(html)} bytes)")
                time.sleep(config.DELAY_BETWEEN_REAL_REQUESTS_SECONDS)
                return FetchResult(url, html, 200, from_cache=False)

            if resp.status_code in config.RETRYABLE_STATUS_CODES and attempt < max_attempts:
                time.sleep(config.RETRY_WAIT_SECONDS)
                continue

            # 404, 403, or any other non-retryable status: log and move on.
            reason = f"http {resp.status_code}"
            self.failed_pages.append({"url": url, "reason": reason})
            time.sleep(config.DELAY_BETWEEN_REAL_REQUESTS_SECONDS)
            return FetchResult(url, None, resp.status_code, from_cache=False, error=reason)

        # Should not reach here, but keep it safe.
        reason = "unknown failure"
        self.failed_pages.append({"url": url, "reason": reason})
        return FetchResult(url, None, None, from_cache=False, error=reason)
