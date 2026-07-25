import os
import requests
from celery.utils.log import get_task_logger

from celery_app import celery_app
from alerts import log_permanent_failure

logger = get_task_logger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


class TemporaryAPIError(Exception):
    """Raised for retryable failures such as timeouts, rate limits, or 5xx errors."""
    pass


@celery_app.task(
    bind=True,
    name="tasks.process_ai_job",
    autoretry_for=(TemporaryAPIError,),
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True,
    max_retries=3,
)
def process_ai_job(self, prompt: str):
    """
    Long-running AI task, executed outside the request/response cycle.
    Temporary failures (timeouts, 429, 5xx) are retried automatically
    with exponential backoff. Permanent failures are logged for
    monitoring via alerts.py and re-raised so the job is marked FAILURE.
    """
    try:
        self.update_state(state="PROGRESS", meta={"step": "sending request to AI provider"})

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        body = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
        }

        response = requests.post(GROQ_URL, headers=headers, json=body, timeout=30)

        if response.status_code in (429, 500, 502, 503, 504):
            raise TemporaryAPIError(f"Temporary upstream error: {response.status_code}")

        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]

        self.update_state(state="PROGRESS", meta={"step": "finalizing result"})
        return {"prompt": prompt, "response": content}

    except TemporaryAPIError as exc:
        logger.warning(f"Job {self.request.id} hit a temporary error, retrying: {exc}")
        raise self.retry(exc=exc)

    except Exception as exc:
        logger.error(f"Job {self.request.id} failed permanently: {exc}")
        log_permanent_failure(job_id=self.request.id, prompt=prompt, error=str(exc))
        raise