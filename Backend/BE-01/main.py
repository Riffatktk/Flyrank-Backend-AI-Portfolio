from fastapi import FastAPI

app = FastAPI(
    title="BE-01 First API",
    description="My first FastAPI backend application for FlyRank AI Internship.",
    version="1.0"
)

@app.get("/")
def root():
    return {
        "message": "Hello! Welcome to my first FastAPI backend.",
        "author": "Riffat"
    }


@app.get("/status")
def status():
    return {
        "status": "success",
        "message": "Backend server is running successfully."
    }