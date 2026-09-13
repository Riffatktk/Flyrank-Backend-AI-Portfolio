"""
Run once after the API is up to create a demo tenant + widget so you have
something to test against immediately.

    python seed.py
"""
import secrets

from app.database import SessionLocal, Base, engine
from app.models import Tenant, Widget

Base.metadata.create_all(bind=engine)

db = SessionLocal()

api_key = secrets.token_hex(16)
tenant = Tenant(name="Demo Tenant", api_key=api_key)
db.add(tenant)
db.commit()
db.refresh(tenant)

widget = Widget(
    tenant_id=tenant.id,
    type="signup_form",
    title="Join our newsletter",
    description="Get weekly updates.",
    fields=["name", "email"],
    button_text="Subscribe",
    display_options={"theme": "light", "position": "bottom-right"},
)
db.add(widget)
db.commit()
db.refresh(widget)

print("Seed complete.")
print(f"  Tenant ID : {tenant.id}")
print(f"  API Key   : {api_key}   (use as X-API-Key header)")
print(f"  Widget ID : {widget.id}")
print(f"  Embed URL : http://localhost:8000/widget.js?id={widget.id}")
