"""
Task API — a small in-memory CRUD API built for FlyRank Internship
Backend Track, Week 2, Assignment A1.

Run with:
    uvicorn main:app --reload

Then visit:
    http://localhost:8000/       -> API description
    http://localhost:8000/docs   -> Swagger UI
"""

from typing import List, Optional
from fastapi import FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A minimal in-memory to-do list API (CRUD) built with FastAPI.",
)


# ---------------------------------------------------------------------------
# Make FastAPI's default validation errors match the spec:
# { "error": "..." } with status 400, instead of FastAPI's default
# { "detail": [...] } with status 422.
# ---------------------------------------------------------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first = exc.errors()[0]
    field = first["loc"][-1] if first.get("loc") else "body"
    return JSONResponse(status_code=400, content={"error": f"Invalid value for '{field}'"})


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

class Task(BaseModel):
    id: int
    title: str
    done: bool = False


class TaskCreate(BaseModel):
    """What the client sends when creating a task."""
    title: str

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("title must not be empty")
        return v.strip()


class TaskUpdate(BaseModel):
    """What the client sends when updating a task."""
    title: Optional[str] = None
    done: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError("title must not be empty")
            return v.strip()
        return v


# ---------------------------------------------------------------------------
# In-memory "database"
# ---------------------------------------------------------------------------

def seed_tasks() -> List[dict]:
    return [
        {"id": 1, "title": "Buy milk", "done": False},
        {"id": 2, "title": "Walk the dog", "done": True},
        {"id": 3, "title": "Finish FlyRank assignment", "done": False},
    ]


tasks: List[dict] = seed_tasks()
next_id: int = 4


# ---------------------------------------------------------------------------
# Stage 1 — root & health
# ---------------------------------------------------------------------------

@app.get("/", tags=["meta"], summary="API description")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", tags=["meta"], summary="Health check")
def health_check():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Stage 2 — Read
# ---------------------------------------------------------------------------

@app.get("/tasks", tags=["tasks"], summary="List tasks (with optional filter/search)")
def list_tasks(done: Optional[bool] = None, search: Optional[str] = None):
    result = tasks
    if done is not None:
        result = [t for t in result if t["done"] == done]
    if search:
        result = [t for t in result if search.lower() in t["title"].lower()]
    return result


@app.get("/tasks/{task_id}", tags=["tasks"], summary="Get one task")
def get_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})


# ---------------------------------------------------------------------------
# Stage 3 — Create
# ---------------------------------------------------------------------------

@app.post("/tasks", status_code=status.HTTP_201_CREATED, tags=["tasks"], summary="Create a task")
def create_task(new_task: TaskCreate):
    global next_id
    task = {"id": next_id, "title": new_task.title, "done": False}
    tasks.append(task)
    next_id += 1
    return task


# ---------------------------------------------------------------------------
# Stage 4 — Update & Delete
# ---------------------------------------------------------------------------

@app.put("/tasks/{task_id}", tags=["tasks"], summary="Update a task")
def update_task(task_id: int, updates: TaskUpdate):
    for t in tasks:
        if t["id"] == task_id:
            if updates.title is None and updates.done is None:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Provide at least one of: title, done"},
                )
            if updates.title is not None:
                t["title"] = updates.title
            if updates.done is not None:
                t["done"] = updates.done
            return t
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})


@app.delete("/tasks/{task_id}", tags=["tasks"], summary="Delete a task")
def delete_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            tasks.remove(t)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})


# ---------------------------------------------------------------------------
# Extras (stretch goals)
# ---------------------------------------------------------------------------

@app.get("/stats", tags=["extras"], summary="Task stats")
def stats():
    total = len(tasks)
    done_count = sum(1 for t in tasks if t["done"])
    return {"total": total, "done": done_count, "open": total - done_count}


@app.post("/reset", tags=["extras"], summary="Reset to the 3 seed tasks")
def reset():
    global tasks, next_id
    tasks = seed_tasks()
    next_id = 4
    return {"status": "reset", "tasks": tasks}
