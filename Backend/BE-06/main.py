from fastapi import FastAPI
from pydantic import BaseModel
from celery.result import AsyncResult

from celery_app import celery_app
from tasks import process_ai_job

app = FastAPI(title="BE-06 Background Job Service")


class JobRequest(BaseModel):
    prompt: str


class JobResponse(BaseModel):
    job_id: str
    status: str


@app.get("/")
def root():
    return {"message": "BE-06 Background Job API is running"}


@app.post("/jobs", response_model=JobResponse)
def submit_job(payload: JobRequest):
    """
    Accepts a request immediately and hands off the long-running
    AI task to a Celery worker. The API never blocks on the AI call.
    """
    task = process_ai_job.delay(payload.prompt)
    return JobResponse(job_id=task.id, status="queued")


@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    """
    Lets the client poll for progress and final result of a
    previously submitted background job.
    """
    result = AsyncResult(job_id, app=celery_app)

    response = {"job_id": job_id, "status": result.status}

    if result.status == "PROGRESS":
        response["meta"] = result.info
    elif result.status == "SUCCESS":
        response["result"] = result.result
    elif result.status == "FAILURE":
        response["error"] = str(result.result)

    return response