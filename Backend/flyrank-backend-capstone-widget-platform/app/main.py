from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import widgets, public, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Embeddable Widget & Lead-Capture Platform",
    description="FlyRank Backend Capstone -- W8",
    version="1.0.0",
)

# The public paths (config, submissions, widget.js) must accept requests from
# ANY origin -- that's the whole premise of an embeddable widget. The admin
# paths are protected separately, by API key, not by CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(widgets.router)
app.include_router(public.router)
app.include_router(dashboard.router)


@app.get("/health")
def health():
    return {"status": "ok"}
