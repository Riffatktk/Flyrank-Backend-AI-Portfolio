import datetime as dt
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_tenant
from app.models import Tenant, Widget, Submission
from app.schemas import DashboardStats, SubmissionOut

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _owned_widget(widget_id: str, tenant: Tenant, db: Session) -> Widget:
    widget = (
        db.query(Widget)
        .filter(Widget.id == widget_id, Widget.tenant_id == tenant.id)
        .first()
    )
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")
    return widget


@router.get("/widgets/{widget_id}/submissions", response_model=list[SubmissionOut])
def list_submissions(
    widget_id: str,
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    _owned_widget(widget_id, tenant, db)  # enforces tenant isolation
    return (
        db.query(Submission)
        .filter(Submission.widget_id == widget_id)
        .order_by(Submission.created_at.desc())
        .all()
    )


@router.get("/widgets/{widget_id}/stats", response_model=DashboardStats)
def widget_stats(
    widget_id: str,
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    _owned_widget(widget_id, tenant, db)

    submissions = db.query(Submission).filter(Submission.widget_id == widget_id).all()

    by_country: dict[str, int] = defaultdict(int)
    last_7_days: dict[str, int] = defaultdict(int)
    today = dt.date.today()

    for s in submissions:
        by_country[s.country or "unknown"] += 1
        days_ago = (today - s.created_at.date()).days
        if 0 <= days_ago < 7:
            last_7_days[s.created_at.date().isoformat()] += 1

    return DashboardStats(
        widget_id=widget_id,
        total_submissions=len(submissions),
        by_country=dict(by_country),
        last_7_days=dict(last_7_days),
    )
