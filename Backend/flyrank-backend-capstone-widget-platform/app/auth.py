from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Tenant

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_current_tenant(
    x_api_key: str = Depends(api_key_header),
    db: Session = Depends(get_db),
) -> Tenant:
    """
    Every authenticated route depends on this. A tenant authenticates with a
    static API key sent in the X-API-Key header. Missing/invalid key -> 401.
    """
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")

    tenant = db.query(Tenant).filter(Tenant.api_key == x_api_key).first()
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return tenant
