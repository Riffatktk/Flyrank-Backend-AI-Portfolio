"""Stage 4: the schema. A record that doesn't match this shape never reaches
books.json — it goes to errors.json with the reason instead."""
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field, field_validator


class BookRecord(BaseModel):
    title: str = Field(min_length=1)
    product_url: HttpUrl          # canonical identity of the record
    price_text: str = Field(min_length=1)
    price_gbp: float = Field(gt=0)
    availability_text: str = Field(min_length=1)
    rating_text: str = Field(min_length=1)
    description: Optional[str] = None
    source_page: HttpUrl
    fetched_at: str

    @field_validator("title", "availability_text", "rating_text")
    @classmethod
    def not_blank(cls, v):
        if not v or not v.strip():
            raise ValueError("must not be blank")
        return v
