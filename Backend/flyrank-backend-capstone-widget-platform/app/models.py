import uuid
import datetime as dt

from sqlalchemy import (
    Column, String, Boolean, ForeignKey, DateTime, JSON, Text
)
from sqlalchemy.orm import relationship

from app.database import Base


def gen_id() -> str:
    return uuid.uuid4().hex[:12]


class Tenant(Base):
    """A customer account. Every widget and submission belongs to exactly one tenant."""
    __tablename__ = "tenants"

    id = Column(String, primary_key=True, default=gen_id)
    name = Column(String, nullable=False)
    api_key = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    widgets = relationship("Widget", back_populates="tenant", cascade="all, delete-orphan")


class Widget(Base):
    """A widget config a tenant creates and embeds on external sites."""
    __tablename__ = "widgets"

    id = Column(String, primary_key=True, default=gen_id)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)

    type = Column(String, nullable=False)          # signup_form | cta | popover
    title = Column(String, nullable=False)
    description = Column(String, default="")
    fields = Column(JSON, default=list)             # e.g. ["name", "email"]
    button_text = Column(String, default="Submit")
    display_options = Column(JSON, default=dict)    # position, delay_seconds, theme...

    bundle_version = Column(String, default="v1")   # bumped on release -> cache-busting
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)

    tenant = relationship("Tenant", back_populates="widgets")
    submissions = relationship("Submission", back_populates="widget", cascade="all, delete-orphan")


class Submission(Base):
    """A single visitor submission captured from a public, cross-origin page."""
    __tablename__ = "submissions"

    id = Column(String, primary_key=True, default=gen_id)
    widget_id = Column(String, ForeignKey("widgets.id"), nullable=False, index=True)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)

    data = Column(JSON, nullable=False)              # validated form fields
    ip_address = Column(String, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    geo_provider = Column(String, nullable=True)      # which provider enriched it, if any

    email_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow, index=True)

    widget = relationship("Widget", back_populates="submissions")
