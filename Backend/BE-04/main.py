import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from repository import InMemoryRepository, PostgresRepository

app = FastAPI(title="BE-04 Containerized Backend")


# -----------------------------
# Pydantic Models
# -----------------------------

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = ""


# -----------------------------
# Repository Selection
# -----------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    repo = PostgresRepository(DATABASE_URL)
    print("Using PostgreSQL Repository")
else:
    repo = InMemoryRepository()
    print("Using In-Memory Repository")


# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def root():
    return {
        "message": "Welcome to BE-04 Containerized Backend!",
        "database": "PostgreSQL" if DATABASE_URL else "In-Memory"
    }


@app.post("/items")
def create_item(item: ItemCreate):
    return repo.create(item.name, item.description)


@app.get("/items")
def get_items():
    return repo.get_all()


@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = repo.get_by_id(item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item