# FlyRank A9 — The Polite Scraper

A small, production-shaped scraping pipeline: it downloads the first 3 catalogue pages of [Books to Scrape](https://books.toscrape.com), visits all 60 book pages, and turns the raw HTML into clean, schema-validated JSON — politely, without crashing on a broken page, and with an honest report at the end of every run.

**Lane:** Python — `requests`, `BeautifulSoup`, `Pydantic`

## Pipeline

```
fetch → extract → normalize → validate → store → report
```

Each stage is independently testable and provable: fetch proves a page arrived, extract proves the right fields were found, validate proves every record is safe to store, and the run report proves the whole thing actually worked.

## Target classification

- **Site:** `books.toscrape.com` — a public sandbox built specifically for scraping practice (confirmed on the site's own "About" text at toscrape.com).
- **Scope:** the first 3 catalogue pages and the 60 book pages they link to. Nothing else on the site is touched.
- **Data collected:** title, price, availability, star rating, description, plus provenance (source page and fetch time) for each book.
- **robots.txt result:** `<paste the output of python -m src.check_robots here>`

I will not reuse this code on another site without checking its rules and terms first.

## Project structure

```
scraper/
├── src/
│   ├── config.py        # politeness settings: user-agent, timeout, delay
│   ├── fetch.py          # fetch + cache, retry logic, failure tracking
│   ├── extract.py        # catalogue + book-detail HTML parsing
│   ├── normalize.py      # price_text -> price_gbp
│   ├── schema.py          # Pydantic record schema
│   ├── storage.py         # idempotent JSON writes
│   ├── report.py          # run-report.json
│   ├── check_robots.py    # one-off robots.txt check
│   └── main.py             # orchestrates all stages
├── tests/                  # offline parser tests (fixtures, no network)
├── requirements.txt
└── README.md
```

## Setup and usage

```bash
# 1. Install dependencies
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Check robots.txt once (Stage 0)
- **robots.txt result:** `404 — no robots file found`

# 3. Run the full pipeline
python -m src.main

# 4. Prove failures don't take the run down (Stage 5)
python -m src.main --inject-fake-url

# 5. Run the offline parser tests
pytest tests/ -v
```

The first run fetches and caches every page under `cache/` (gitignored). Every run after that reads from the cache, so repeated development runs never hit the live site again.

## Politeness rules

| Rule | Implementation |
|---|---|
| Identify the bot | Custom `User-Agent` naming the project and a repo link |
| Don't hang forever | 8-second timeout on every real request |
| Verify before parsing | Only a `200` status is treated as a valid page |
| Don't hammer the site | 0.6s delay between real requests; cached reads have no delay |
| Fail gracefully | One retry on timeout/`5xx`; never retries `404`/`403` |

## Record schema

```json
{
  "title": "A Light in the Attic",
  "product_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "price_text": "£51.77",
  "price_gbp": 51.77,
  "availability_text": "In stock (22 available)",
  "rating_text": "Three",
  "description": "...",
  "source_page": "https://books.toscrape.com/catalogue/page-1.html",
  "fetched_at": "2026-08-06T10:00:00Z"
}
```

`product_url` is each record's canonical identity. Records are deduped by it before writing, so re-running the pipeline always produces the same 60 records — never 120.

Records that fail schema validation are written to `output/errors.json` with the reason, instead of silently entering `output/books.json`.
```

`product_url` is each record's canonical identity. Records are deduped by it before writing, so re-running the pipeline always produces the same 60 records — never 120.

Records that fail schema validation are written to `output/errors.json` with the reason, instead of silently entering `output/books.json`.

## Sample run report

```json
## Sample run report

```json
{
  "start_time": "2026-09-09T10:28:05.242146+00:00",
  "end_time": "2026-09-09T10:29:08.529155+00:00",
  "duration_seconds": 63.29,
  "catalogue_pages": 3,
  "pages_fetched": 63,
  "cache_hits": 0,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 0,
  "failed_page_details": []
}
```

*(Replace with your own output from `output/run-report.json` before submitting.)*

No browser was needed for this assignment: the data is already present in the HTML the server sends, so a headless browser would only add cost with no benefit.

## Ethics note

Use an official API instead of scraping whenever one exists. Never bypass logins, paywalls, or explicit blocks. Collect only the data actually needed for the task — here, the eight fields above, from a sandbox built for exactly this purpose.

## Known limitation

`source_page` currently records the first catalogue page for every book rather than the exact page it was discovered on (1, 2, or 3). This is sufficient provenance for this assignment's scope; a production pipeline would track it per URL.

## Author

Riffat · [github.com/Riffatktk](https://github.com/Riffatktk)