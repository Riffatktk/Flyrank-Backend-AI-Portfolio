from typing import Optional
from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    done: bool = False


class TaskCreate(SQLModel):
    title: str


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    done: Optional[bool] = None