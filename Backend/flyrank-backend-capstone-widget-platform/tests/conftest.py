import os
import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.main import app
from app.database import SessionLocal, Base, engine
from app.models import Tenant

Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def tenant_and_key():
    db = SessionLocal()
    tenant = Tenant(name="Test Tenant", api_key="test-key-123")
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    yield tenant, "test-key-123"
    db.query(Tenant).filter(Tenant.id == tenant.id).delete()
    db.commit()
    db.close()
