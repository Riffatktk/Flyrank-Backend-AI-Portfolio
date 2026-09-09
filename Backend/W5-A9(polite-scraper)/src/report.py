"""Stage 5: end every run with a few honest numbers."""
import json
import os
from datetime import datetime, timezone


def write_run_report(path, *, start_time, catalogue_pages, pages_fetched,
                      cache_hits, valid_records, invalid_records, failed_pages):
    end_time = datetime.now(timezone.utc)
    report = {
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_seconds": round((end_time - start_time).total_seconds(), 2),
        "catalogue_pages": catalogue_pages,
        "pages_fetched": pages_fetched,
        "cache_hits": cache_hits,
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "failed_pages": len(failed_pages),
        "failed_page_details": failed_pages,
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    return report
