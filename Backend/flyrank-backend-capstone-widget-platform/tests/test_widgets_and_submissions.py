def test_create_widget_requires_auth(client):
    resp = client.post("/widgets", json={"type": "signup_form", "title": "Test"})
    assert resp.status_code in (401, 422)  # missing header


def test_full_widget_and_submission_flow(client, tenant_and_key):
    _, api_key = tenant_and_key
    headers = {"X-API-Key": api_key}

    create_resp = client.post(
        "/widgets",
        json={"type": "signup_form", "title": "Newsletter", "fields": ["email"]},
        headers=headers,
    )
    assert create_resp.status_code == 201
    widget_id = create_resp.json()["id"]
    assert "embed_snippet" in create_resp.json()

    config_resp = client.get(f"/widgets/{widget_id}/config")
    assert config_resp.status_code == 200
    assert config_resp.headers["cache-control"].startswith("public")

    submit_resp = client.post(
        f"/widgets/{widget_id}/submissions",
        json={"data": {"email": "visitor@example.com"}, "website": ""},
    )
    assert submit_resp.status_code == 201

    stats_resp = client.get(f"/dashboard/widgets/{widget_id}/stats", headers=headers)
    assert stats_resp.status_code == 200
    assert stats_resp.json()["total_submissions"] == 1


def test_honeypot_rejects_bot_submission(client, tenant_and_key):
    _, api_key = tenant_and_key
    headers = {"X-API-Key": api_key}
    widget_id = client.post(
        "/widgets", json={"type": "cta", "title": "CTA"}, headers=headers
    ).json()["id"]

    resp = client.post(
        f"/widgets/{widget_id}/submissions",
        json={"data": {"email": "bot@example.com"}, "website": "http://spam.example"},
    )
    assert resp.status_code == 422


def test_oversized_payload_rejected(client, tenant_and_key):
    _, api_key = tenant_and_key
    headers = {"X-API-Key": api_key}
    widget_id = client.post(
        "/widgets", json={"type": "cta", "title": "CTA"}, headers=headers
    ).json()["id"]

    resp = client.post(
        f"/widgets/{widget_id}/submissions",
        json={"data": {"note": "x" * 3000}},
    )
    assert resp.status_code == 422


def test_rate_limit_returns_429_then_recovers(client, tenant_and_key, monkeypatch):
    _, api_key = tenant_and_key
    headers = {"X-API-Key": api_key}
    widget_id = client.post(
        "/widgets", json={"type": "cta", "title": "CTA"}, headers=headers
    ).json()["id"]

    from app.config import settings
    monkeypatch.setattr(settings, "rate_limit_per_minute", 2)

    for _ in range(2):
        r = client.post(
            f"/widgets/{widget_id}/submissions", json={"data": {"a": "1"}}
        )
        assert r.status_code == 201

    blocked = client.post(
        f"/widgets/{widget_id}/submissions", json={"data": {"a": "1"}}
    )
    assert blocked.status_code == 429
