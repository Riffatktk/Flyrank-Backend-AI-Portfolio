from fastapi import FastAPI

app = FastAPI(title="FlyRank A4 Auth API")


@app.get("/")
def root():
    return {"message": "FlyRank A4 Auth API is running"}