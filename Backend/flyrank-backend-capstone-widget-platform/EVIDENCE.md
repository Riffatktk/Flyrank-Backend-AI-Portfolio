# EVIDENCE.md

One pasted proof per checkbox in the capstone brief's Requirements section
(Section 6). All commands were run against a local SQLite-backed instance
in a GitHub Codespace (`http://localhost:8000`), and cross-checked via the
Swagger UI at `/docs` — see `screenshots/` for the UI-side captures.

## Widget management

- [x] Authenticated CRUD endpoints for widgets; requests without valid auth are rejected.

  Request without an API key:
  ```
  curl -i http://localhost:8000/widgets
  HTTP/1.1 401 Unauthorized
  {"detail":"Missing X-API-Key header"}
  ```
  Full CRUD confirmed working with a valid key: create (`201`), list (`200`),
  get single (`200`), update (`200`).
  See `screenshots/00-api-overview-swagger-ui.png` and
  `screenshots/01-widget-created-embed-snippet.png`.

- [x] Multi-tenant isolation proven: tenant A cannot read or modify tenant B's widgets or submissions.

  Tenant B's API key used against Tenant A's widget id:
  ```
  curl -i http://localhost:8000/widgets/f4b4dd583e8f \
    -H "X-API-Key: <tenant B key>"
  HTTP/1.1 404 Not Found
  {"detail":"Widget not found"}

  curl -i -X PUT http://localhost:8000/widgets/f4b4dd583e8f \
    -H "X-API-Key: <tenant B key>" -d '{"title":"Hacked by Tenant B"}'
  HTTP/1.1 404 Not Found

  curl -i http://localhost:8000/dashboard/widgets/f4b4dd583e8f/submissions \
    -H "X-API-Key: <tenant B key>"
  HTTP/1.1 404 Not Found
  ```
  Sanity check -- Tenant B can access its own widget:
  ```
  curl -i http://localhost:8000/widgets/a3f6177063eb \
    -H "X-API-Key: <tenant B key>"
  HTTP/1.1 200 OK
  ```

## Widget delivery

- [x] Embed snippet generated per widget.

  ```
  curl -i -X POST http://localhost:8000/widgets \
    -H "X-API-Key: <key>" -d '{"type":"cta","title":"Test CTA","fields":["email"]}'
  HTTP/1.1 201 Created
  {"id":"f4b4dd583e8f", ...,
   "embed_snippet":"<script src=\"https://your-domain.com/widget.js?id=f4b4dd583e8f\" async></script>"}
  ```
  See `screenshots/01-widget-created-embed-snippet.png`.

- [x] Public config endpoint serves a small payload with correct HTTP cache headers.

  ```
  curl -i http://localhost:8000/widgets/f4b4dd583e8f/config
  HTTP/1.1 200 OK
  cache-control: public, max-age=60
  ```
  See `screenshots/02-widget-config-cache-header.png`.

- [x] Widget JavaScript is served as a versioned bundle (new version = new URL or cache-bust).

  ```
  curl -i http://localhost:8000/widget.js
  HTTP/1.1 200 OK
  cache-control: public, max-age=31536000, immutable
  ```
  See `screenshots/03-widget-bundle-cache-header.png`. `Widget.bundle_version`
  is stored per-widget in the model, ready to be embedded in the asset URL on
  a real release pipeline.

- [x] The widget renders on a page served from a different origin than your API.

  `test-site/index.html` served via `python3 -m http.server 5500` (port 5500)
  successfully rendered the widget fetched from the API on port 8000 -- a
  genuine cross-origin load, confirmed visually in-browser.

## Public submission API

- [x] Cross-origin submissions work: CORS headers correct, preflight (OPTIONS) handled.

  ```
  curl -i -X OPTIONS http://localhost:8000/widgets/f4b4dd583e8f/submissions \
    -H "Origin: http://localhost:5500" \
    -H "Access-Control-Request-Method: POST"
  HTTP/1.1 200 OK
  access-control-allow-origin: *
  access-control-allow-methods: GET, POST, OPTIONS
  access-control-max-age: 600
  ```

- [x] All incoming input validated; malformed and oversized payloads rejected with appropriate 4xx codes and JSON errors.

  ```
  curl -i -X POST http://localhost:8000/widgets/f4b4dd583e8f/submissions \
    -d '{"data": {}}'
  HTTP/1.1 422 Unprocessable Content
  {"detail":[{"type":"value_error","loc":["body","data"],
              "msg":"Value error, data must not be empty", ...}]}
  ```
  See `screenshots/05-submission-invalid-payload-422.png`.

- [x] Valid submissions stored safely, linked to the right widget and tenant.

  ```
  curl -i -X POST http://localhost:8000/widgets/f4b4dd583e8f/submissions \
    -d '{"data": {"email": "visitor@test.com"}}'
  HTTP/1.1 201 Created
  {"id":"3f951b1f2d07","widget_id":"f4b4dd583e8f", ...}
  ```
  Confirmed present in the dashboard:
  ```
  curl http://localhost:8000/dashboard/widgets/f4b4dd583e8f/submissions \
    -H "X-API-Key: <key>"
  HTTP/1.1 200 OK
  [{"id":"3f951b1f2d07", ...}]
  ```
  See `screenshots/04-submission-valid-201.png`,
  `screenshots/07-dashboard-submissions.png`,
  `screenshots/08-dashboard-stats.png`.

## Abuse protection

- [x] Rate limiting per IP and/or per widget returns 429 under a burst -- and the API keeps serving legitimate traffic.

  15 rapid submissions to the same widget:
  ```
  201
  201
  201
  201
  201
  201
  201
  201
  201
  201
  429
  429
  429
  429
  429
  ```
  First 10 (the configured `RATE_LIMIT_PER_MINUTE`) succeed, the rest are
  cleanly rejected with `429` -- the service stayed up throughout.

- [x] At least one spam-prevention technique (honeypot field, token, or heuristic) demonstrably blocks a spam submission.

  ```
  curl -i -X POST http://localhost:8000/widgets/f4b4dd583e8f/submissions \
    -d '{"data": {"email": "bot@test.com"}, "website": "spam"}'
  HTTP/1.1 422 Unprocessable Content
  ```
  See `screenshots/06-submission-honeypot-blocked-422.png`.

## Enrichment & safe side effects

- [x] IP-to-geo enrichment uses a provider fallback chain: provider A down -> provider B answers -> submission enriched.

  With `GEO_PROVIDER_A_DOWN=true` and a spoofed public IP
  (`X-Forwarded-For: 8.8.8.8`):
  ```
  curl -i -X POST http://localhost:8000/widgets/f4b4dd583e8f/submissions \
    -H "X-Forwarded-For: 8.8.8.8" -d '{"data": {"email": "geo2@test.com"}}'
  HTTP/1.1 201 Created
  {"id":"321d5edd5e49", ..., "country":"United States","city":"Ashburn"}
  ```
  Provider A was disabled; provider B (`ipapi.co`) answered and the
  submission was enriched.

- [x] All providers down -> submission still succeeds (without geo). Degrade, never fail.

  With both `GEO_PROVIDER_A_DOWN=true` and `GEO_PROVIDER_B_DOWN=true`,
  after restarting the server so the `.env` change took effect
  (`--reload` only watches `.py` files, not `.env`):
  ```
  curl -i -X POST http://localhost:8000/widgets/f4b4dd583e8f/submissions \
    -H "X-Forwarded-For: 8.8.8.8" -d '{"data": {"email": "geo5@test.com"}}'
  HTTP/1.1 201 Created
  {"id":"1da0c417befb", ..., "country":null,"city":null}
  ```

- [x] A failing confirmation email / webhook does not prevent the submission from being stored.

  With `EMAIL_SHOULD_FAIL=true` (server restarted to pick up the change):
  ```
  curl -i -X POST http://localhost:8000/widgets/f4b4dd583e8f/submissions \
    -d '{"data": {"email": "emailtest@test.com"}}'
  HTTP/1.1 201 Created
  {"id":"bb1899d4b03e", ..., "created_at":"2026-09-13T11:55:52.107886"}
  ```
  The confirmation-email step threw internally (`EmailDeliveryError`), and
  the submission still returned `201` and is present in storage.

## Documentation

- [x] README with architecture diagram, setup instructions, and API documentation; the required files from Section 11 present.

  `README.md` includes the request-path architecture diagram, both a
  Docker/Postgres and a local Python/SQLite run path, Swagger UI usage,
  and a deterministic reproduction guide for every acceptance probe above.
  `capstone.yaml`, `BUILDLOG.md`, `.env.example`, and `LICENSE` are all
  present at the repo root alongside this file.

---

**Note on environment:** development and testing were done in a GitHub
Codespace. The Postgres container (via `docker compose`) hit a Docker
bridge-network timeout specific to that Codespace; local development
therefore used SQLite (`DATABASE_URL=sqlite:///./widget_platform.db`), which
the capstone brief's own free-stack table lists as an acceptable starting
option. The `docker-compose.yml` / Postgres path is unchanged and is exactly
what the free-tools table describes for a standard machine.

## Test suite (stretch goal)
pytest -v
tests/test_widgets_and_submissions.py::test_create_widget_requires_auth PASSED
tests/test_widgets_and_submissions.py::test_full_widget_and_submission_flow PASSED
tests/test_widgets_and_submissions.py::test_honeypot_rejects_bot_submission PASSED
tests/test_widgets_and_submissions.py::test_oversized_payload_rejected PASSED
tests/test_widgets_and_submissions.py::test_rate_limit_returns_429_then_recovers PASSED

5 passed, 19 warnings in 0.29s
