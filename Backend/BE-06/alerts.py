import json
import logging
from datetime import datetime, timezone

logging.basicConfig(
    filename="permanent_failures.log",
    level=logging.ERROR,
    format="%(asctime)s %(message)s",
)


def log_permanent_failure(job_id: str, prompt: str, error: str) -> None:
    """
    Records a permanent (non-retryable) job failure for monitoring.
    In production this could be swapped for a webhook, email, or
    Slack alert instead of a local log file.
    """
    entry = {
        "job_id": job_id,
        "prompt": prompt,
        "error": error,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    logging.error(json.dumps(entry))
    print(f"[ALERT] Permanent failure logged for job {job_id}: {error}")