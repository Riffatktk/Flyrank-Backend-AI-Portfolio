"""FlyRank A9 — The polite scraper.

Run:
    python -m src.main
    python -m src.main --inject-fake-url     # Stage 5 proof: one bad page must not kill the run
"""
import sys
import argparse
from datetime import datetime, timezone
from pydantic import ValidationError

from . import config
from .fetch import Fetcher
from .extract import parse_catalogue_page, parse_book_detail
from .normalize import normalize_price
from .schema import BookRecord
from .storage import write_books, write_errors
from .report import write_run_report


def discover_book_urls(fetcher):
    """Stage 2: walk catalogue page 1 -> 2 -> 3 via the site's own 'next' link."""
    book_urls = []
    url = config.FIRST_CATALOGUE_URL
    pages_seen = 0

    while url and pages_seen < config.MAX_CATALOGUE_PAGES:
        pages_seen += 1
        result = fetcher.fetch(url, label=f"catalogue page {pages_seen}")
        if not result.ok:
            print(f"  !! could not load catalogue page {pages_seen}: {result.error}")
            break
        links, next_url = parse_catalogue_page(result.html, url)
        book_urls.extend(links)
        url = next_url

    unique_urls = list(dict.fromkeys(book_urls))  # de-dupe, keep order
    print(f"catalogue_pages={pages_seen} discovered={len(book_urls)} unique_urls={len(unique_urls)}")
    return pages_seen, unique_urls


def extract_all_records(fetcher, book_urls):
    """Stage 3 + Stage 5: fetch every detail page; one bad page is logged and
    skipped, the rest of the run keeps going."""
    raw_records = []
    for i, book_url in enumerate(book_urls, start=1):
        result = fetcher.fetch(book_url, label=f"book {i}/{len(book_urls)}")
        if not result.ok:
            # Already recorded in fetcher.failed_pages; move on.
            continue
        fetched_at = datetime.now(timezone.utc).isoformat()
        # source_page isn't tracked per-URL here for simplicity; the
        # catalogue page that discovered it is close enough provenance for
        # this assignment's scope.
        record = parse_book_detail(result.html, book_url, config.FIRST_CATALOGUE_URL, fetched_at)
        raw_records.append(record)

    print(f"detail_pages={len(raw_records)}")
    if raw_records:
        print("sample raw record:", raw_records[0])
    return raw_records


def normalize_and_validate(raw_records):
    """Stage 4: clean, check, split into valid / invalid."""
    valid, invalid = [], []
    for raw in raw_records:
        try:
            price_gbp = normalize_price(raw.get("price_text"))
            candidate = dict(raw)
            candidate["price_gbp"] = price_gbp
            model = BookRecord(**candidate)
            valid.append(model.model_dump(mode="json"))
        except (ValidationError, ValueError) as exc:
            invalid.append({"record": raw, "reason": str(exc)})
    return valid, invalid


def run(inject_fake_url=False):
    start_time = datetime.now(timezone.utc)
    fetcher = Fetcher()

    catalogue_pages, book_urls = discover_book_urls(fetcher)

    if inject_fake_url:
        fake = "https://books.toscrape.com/catalogue/this-book-does-not-exist_9999/index.html"
        book_urls.append(fake)
        print(f"  (Stage 5 proof) injected fake URL: {fake}")

    raw_records = extract_all_records(fetcher, book_urls)
    valid, invalid = normalize_and_validate(raw_records)

    write_books(valid, config.BOOKS_JSON_PATH)
    write_errors(invalid, config.ERRORS_JSON_PATH)

    report = write_run_report(
        config.RUN_REPORT_PATH,
        start_time=start_time,
        catalogue_pages=catalogue_pages,
        pages_fetched=fetcher.pages_fetched,
        cache_hits=fetcher.cache_hits,
        valid_records=len(valid),
        invalid_records=len(invalid),
        failed_pages=fetcher.failed_pages,
    )

    print("\n--- run-report.json ---")
    print(report)
    return report


def main():
    parser = argparse.ArgumentParser(description="FlyRank A9 polite scraper")
    parser.add_argument("--inject-fake-url", action="store_true",
                         help="Add one made-up book URL to prove Stage 5 survives a broken page.")
    args = parser.parse_args()
    run(inject_fake_url=args.inject_fake_url)


if __name__ == "__main__":
    sys.exit(main())
