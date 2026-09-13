import datetime as dt
from typing import Optional, Any

from pydantic import BaseModel, Field, field_validator


# ---------- Widgets ----------

class WidgetCreate(BaseModel):
    type: str = Field(..., pattern="^(signup_form|cta|popover)$")
    title: str = Field(..., min_length=1, max_length=120)
    description: str = Field("", max_length=500)
    fields: list[str] = Field(default_factory=lambda: ["name", "email"])
    button_text: str = Field("Submit", max_length=40)
    display_options: dict = Field(default_factory=dict)


class WidgetUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=500)
    fields: Optional[list[str]] = None
    button_text: Optional[str] = Field(None, max_length=40)
    display_options: Optional[dict] = None


class WidgetOut(BaseModel):
    id: str
    type: str
    title: str
    description: str
    fields: list[str]
    button_text: str
    display_options: dict
    bundle_version: str
    embed_snippet: str

    class Config:
        from_attributes = True


# ---------- Public submission ----------

class SubmissionIn(BaseModel):
    data: dict[str, Any]
    # honeypot: real visitors never fill this; bots frequently do
    website: Optional[str] = Field(default="", max_length=200)

    @field_validator("data")
    @classmethod
    def data_not_empty_or_oversized(cls, v):
        if not v:
            raise ValueError("data must not be empty")
        if len(v) > 30:
            raise ValueError("too many fields")
        for key, val in v.items():
            if isinstance(val, str) and len(val) > 2000:
                raise ValueError(f"field '{key}' exceeds max length")
        return v


class SubmissionOut(BaseModel):
    id: str
    widget_id: str
    data: dict
    country: Optional[str]
    city: Optional[str]
    created_at: dt.datetime

    class Config:
        from_attributes = True


# ---------- Dashboard ----------

class DashboardStats(BaseModel):
    widget_id: str
    total_submissions: int
    by_country: dict[str, int]
    last_7_days: dict[str, int]
