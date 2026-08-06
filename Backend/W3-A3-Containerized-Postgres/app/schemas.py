from typing import Optional
from sqlmodel import SQLModel


class TaskCreate(SQLModel):
    title: str


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    done: Optional[bool] = None