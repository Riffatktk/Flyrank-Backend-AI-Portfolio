from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

from auth import supabase

app = FastAPI(title="FlyRank A4 Auth API")


class AuthRequest(BaseModel):
    email: str
    password: str


@app.get("/")
def root():
    return {"message": "FlyRank A4 Auth API is running"}


# =========================
# Stage 1 — Signup
# =========================

@app.post("/auth/signup", status_code=201)
def signup(data: AuthRequest):
    if not data.email or not data.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password
        })

        return {
            "user": response.user
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =========================
# Stage 1 — Login
# =========================

@app.post("/auth/login")
def login(data: AuthRequest):
    if not data.email or not data.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials"
        )


# =========================
# Stage 2 — Public Route
# =========================

@app.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }


# =========================
# Stage 2 — Protected Route
# =========================

@app.get("/protected/profile")
def protected_profile(
    authorization: str | None = Header(default=None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    token = authorization.replace("Bearer ", "", 1).strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    try:
        response = supabase.auth.get_user(token)
        user = response.user

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

        return {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )