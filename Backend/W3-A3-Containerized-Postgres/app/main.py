"""
Task API — FastAPI CRUD API with PostgreSQL + SQLModel
Backend Track — Week 3 A3
Run:
    uvicorn main:app --reload --port 8000
Docs:
    http://127.0.0.1:8001/docs
"""

from typing import Optional

from fastapi import FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from sqlmodel import Session, select

from database import engine, create_db_and_tables
from models import Task as DBTask


app = FastAPI(
    title="Task API",
    version="1.0",
   description="A CRUD Task API built using FastAPI, SQLModel and PostgreSQL.",
)


# --------------------------------------------------
# Database startup
# --------------------------------------------------

@app.on_event("startup")
def startup():
    create_db_and_tables()

    with Session(engine) as session:
        if session.exec(select(DBTask)).first() is None:
            session.add(DBTask(title="Buy milk", done=False))
            session.add(DBTask(title="Walk the dog", done=True))
            session.add(DBTask(title="Finish FlyRank assignment", done=False))

            session.commit()


# --------------------------------------------------
# Validation Error Handler
# --------------------------------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    first_error = exc.errors()[0]
    field = first_error["loc"][-1]

    return JSONResponse(
        status_code=400,
        content={
            "error": f"Invalid value for '{field}'"
        }
    )


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class TaskCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, value):
        if not value.strip():
            raise ValueError("title must not be empty")

        return value.strip()


class TaskUpdate(BaseModel):

    title: Optional[str] = None
    done: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, value):

        if value is not None:

            if not value.strip():
                raise ValueError("title must not be empty")

            return value.strip()

        return value



# --------------------------------------------------
# Root & Health
# --------------------------------------------------

@app.get("/")
def read_root():

    return {
        "name": "Task API",
        "version": "1.0",
        "database": "PostgreSQL"
    }


@app.get("/health")
def health_check():

    return {
        "status": "ok"
    }



# --------------------------------------------------
# CRUD Endpoints
# --------------------------------------------------

@app.get("/tasks")
def list_tasks():

    with Session(engine) as session:

        tasks = session.exec(select(DBTask)).all()

        return tasks



@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    with Session(engine) as session:

        task = session.get(DBTask, task_id)

        if task is None:

            return JSONResponse(
                status_code=404,
                content={
                    "error": f"Task {task_id} not found"
                }
            )

        return task



@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED
)
def create_task(task_data: TaskCreate):

    with Session(engine) as session:

        task = DBTask(
            title=task_data.title,
            done=False
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        return task



@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    updates: TaskUpdate
):

    with Session(engine) as session:

        task = session.get(DBTask, task_id)

        if task is None:

            return JSONResponse(
                status_code=404,
                content={
                    "error": f"Task {task_id} not found"
                }
            )


        if updates.title is None and updates.done is None:

            return JSONResponse(
                status_code=400,
                content={
                    "error": "Provide at least one of: title, done"
                }
            )


        if updates.title is not None:
            task.title = updates.title


        if updates.done is not None:
            task.done = updates.done


        session.add(task)
        session.commit()
        session.refresh(task)

        return task



@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    with Session(engine) as session:

        task = session.get(DBTask, task_id)

        if task is None:

            return JSONResponse(
                status_code=404,
                content={
                    "error": f"Task {task_id} not found"
                }
            )


        session.delete(task)
        session.commit()

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )



# --------------------------------------------------
# Extra Endpoint
# --------------------------------------------------

@app.get("/stats")
def stats():

    with Session(engine) as session:

        tasks = session.exec(select(DBTask)).all()

        total = len(tasks)
        done = sum(task.done for task in tasks)

        return {
            "total": total,
            "done": done,
            "pending": total - done
        }