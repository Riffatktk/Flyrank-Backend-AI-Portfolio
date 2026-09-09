"""Writes output/books.json and output/errors.json.

Idempotency lives here: records are deduped by their canonical product_url
before writing, so running the pipeline twice yields the same 60 records,
never 120.
"""
import json
import os


def dedupe_by_url(records):
    """Keep the first record seen per product_url, preserve order."""
    seen = {}
    for rec in records:
        url = str(rec["product_url"])
        if url not in seen:
            seen[url] = rec
    return list(seen.values())


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_books(records, path):
    deduped = dedupe_by_url(records)
    write_json(path, deduped)
    return len(deduped)


def write_errors(errors, path):
    write_json(path, errors)
    return len(errors)
