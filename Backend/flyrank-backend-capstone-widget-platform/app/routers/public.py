"""
The three public request paths a random website visitor's browser will hit:

  GET  /widgets/{id}/config  -- public, cached, CORS
  POST /submissions          -- public, CORS, validated, rate-limited, protected
  GET  /widget.js            -- versioned static bundle, long cache
"""
import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Widget, Submission
from app.schemas import SubmissionIn, SubmissionOut
from app.services.ratelimit import is_rate_limited
from app.services.geo import enrich_ip
from app.services.email_service import send_confirmation, EmailDeliveryError

router = APIRouter(tags=["public"])


@router.get("/widgets/{widget_id}/config")
def get_widget_config(widget_id: str, response: Response, db: Session = Depends(get_db)):
    widget = db.query(Widget).filter(Widget.id == widget_id).first()
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")

    # Short-lived cache: config can change, so don't cache long
    response.headers["Cache-Control"] = "public, max-age=60"

    return {
        "id": widget.id,
        "type": widget.type,
        "title": widget.title,
        "description": widget.description,
        "fields": widget.fields,
        "button_text": widget.button_text,
        "display_options": widget.display_options,
        "bundle_version": widget.bundle_version,
    }


@router.get("/widget.js")
def get_widget_bundle(response: Response):
    # Versioned/immutable long cache: this file only changes on release.
    response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    return FileResponse("static/widget.js", media_type="application/javascript")


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@router.post("/widgets/{widget_id}/submissions", response_model=SubmissionOut, status_code=201)
def create_submission(
    widget_id: str,
    payload: SubmissionIn,
    request: Request,
    db: Session = Depends(get_db),
):
    widget = db.query(Widget).filter(Widget.id == widget_id).first()
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")

    # --- Spam control: honeypot. Real visitors never see/fill this field. ---
    if payload.website:
        raise HTTPException(status_code=422, detail="Rejected")

    ip = _client_ip(request)

    # --- Abuse protection: rate limit per IP+widget ---
    if is_rate_limited(ip, widget_id):
        raise HTTPException(status_code=429, detail="Too many submissions, slow down")

    # --- Enrichment: fallback chain, never blocks storage on failure ---
    geo = enrich_ip(ip)

    submission = Submission(
        widget_id=widget.id,
        tenant_id=widget.tenant_id,
        data=payload.data,
        ip_address=ip,
        country=geo["country"] if geo else None,
        city=geo["city"] if geo else None,
        geo_provider=geo["provider"] if geo else None,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # --- Safe side effect: failure here must NOT fail the response ---
    try:
        send_confirmation(submission.id, widget.title)
        submission.email_sent = True
        db.commit()
    except EmailDeliveryError:
        pass  # logged inside the service; submission already succeeded

    return submission
