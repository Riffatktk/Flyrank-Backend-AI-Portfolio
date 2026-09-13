"""
Safe side effect: a confirmation "email" (here: a console log, per the
capstone's $0 stack) sent after a submission is stored.

The caller MUST wrap this in try/except -- failure here must never roll back
or fail the main submission response. That's the whole point of the exercise.
"""
from app.config import settings


class EmailDeliveryError(Exception):
    pass


def send_confirmation(submission_id: str, widget_title: str) -> None:
    if settings.email_should_fail:
        raise EmailDeliveryError("Simulated SMTP failure (EMAIL_SHOULD_FAIL=true)")

    print(f"[email] Confirmation sent for submission {submission_id} "
          f"on widget '{widget_title}'")
