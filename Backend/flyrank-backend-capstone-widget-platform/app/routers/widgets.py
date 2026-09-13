from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_tenant
from app.models import Tenant, Widget
from app.schemas import WidgetCreate, WidgetUpdate, WidgetOut

router = APIRouter(prefix="/widgets", tags=["widget-management"])


def _to_out(widget: Widget, request_base_url: str) -> WidgetOut:
    snippet = (
        f'<script src="{request_base_url}widget.js?id={widget.id}" async></script>'
    )
    return WidgetOut(
        id=widget.id,
        type=widget.type,
        title=widget.title,
        description=widget.description,
        fields=widget.fields,
        button_text=widget.button_text,
        display_options=widget.display_options,
        bundle_version=widget.bundle_version,
        embed_snippet=snippet,
    )


def _get_owned_widget(widget_id: str, tenant: Tenant, db: Session) -> Widget:
    """Tenant isolation lives here: a widget is only findable within its own tenant scope."""
    widget = (
        db.query(Widget)
        .filter(Widget.id == widget_id, Widget.tenant_id == tenant.id)
        .first()
    )
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")
    return widget


@router.post("", response_model=WidgetOut, status_code=201)
def create_widget(
    payload: WidgetCreate,
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    widget = Widget(tenant_id=tenant.id, **payload.model_dump())
    db.add(widget)
    db.commit()
    db.refresh(widget)
    return _to_out(widget, "https://your-domain.com/")


@router.get("", response_model=list[WidgetOut])
def list_widgets(
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    widgets = db.query(Widget).filter(Widget.tenant_id == tenant.id).all()
    return [_to_out(w, "https://your-domain.com/") for w in widgets]


@router.get("/{widget_id}", response_model=WidgetOut)
def get_widget(
    widget_id: str,
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    widget = _get_owned_widget(widget_id, tenant, db)
    return _to_out(widget, "https://your-domain.com/")


@router.put("/{widget_id}", response_model=WidgetOut)
def update_widget(
    widget_id: str,
    payload: WidgetUpdate,
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    widget = _get_owned_widget(widget_id, tenant, db)
    updates = payload.model_dump(exclude_unset=True)
    for k, v in updates.items():
        setattr(widget, k, v)
    db.commit()
    db.refresh(widget)
    return _to_out(widget, "https://your-domain.com/")


@router.delete("/{widget_id}", status_code=204)
def delete_widget(
    widget_id: str,
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    widget = _get_owned_widget(widget_id, tenant, db)
    db.delete(widget)
    db.commit()
    return None
