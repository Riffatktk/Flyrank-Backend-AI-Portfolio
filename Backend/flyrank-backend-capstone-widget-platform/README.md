# Embeddable Widget & Lead-Capture Platform

FlyRank Backend Track — Capstone (W8)

A platform where a tenant creates an embeddable widget, gets a one-line
`<script>` snippet, and installs it on any external website. Visitor
submissions travel back to this backend, where they're validated,
rate-limited, spam-checked, enriched with geolocation (with a provider
fallback chain), stored, and shown in a dashboard.

## Architecture

```
Widget Owner (X-API-Key auth)
   -> Widget Management API  -> Widgets DB (tenant-isolated)
   -> returns embed snippet

Customer Website (any origin)
   <script src="widget.js?id=123">
   -> GET /widgets/:id/config     (public, cached, CORS)
   -> renders form

Website Visitor
   -> POST /widgets/:id/submissions   (public, CORS)
      | boundary validation      -- bad payload -> 4xx, never 500
      | honeypot + rate limit    -- flood/bot -> 429 / rejected, service stays up
      | geo enrichment           -- ip-api.com -> (fail) -> ipapi.co -> (fail) -> store anyway
      | store submission
      | confirmation "email"     -- failure never blocks the response

Widget Owner (X-API-Key auth)
   -> GET /dashboard/widgets/:id/stats  <- submissions + aggregates
```

## Stack

FastAPI · SQLAlchemy · httpx · plain vanilla JS widget
Database: PostgreSQL (via Docker) in production config, SQLite for local
dev/testing — both are supported by the same `DATABASE_URL` setting (see
"Two ways to run" below).

## Project structure

```
.
├── app/
│   ├── main.py               # app factory, CORS, router wiring
│   ├── config.py              # env-driven settings
│   ├── database.py            # SQLAlchemy engine/session
│   ├── models.py               # Tenant, Widget, Submission
│   ├── schemas.py              # Pydantic request/response models
│   ├── auth.py                 # X-API-Key -> tenant dependency (APIKeyHeader,
│   │                            #   shows up as an "Authorize" button in /docs)
│   ├── routers/
│   │   ├── widgets.py          # authenticated CRUD (tenant-isolated)
│   │   ├── public.py           # config, widget.js, submissions
│   │   └── dashboard.py        # authenticated stats/aggregation
│   └── services/
│       ├── ratelimit.py        # per-IP/widget fixed-window limiter
│       ├── geo.py               # provider A -> B fallback chain
│       └── email_service.py     # safe, best-effort side effect
├── static/widget.js             # the embeddable bundle
├── test-site/index.html         # "customer site" on a second origin
├── seed.py                      # creates a demo tenant + widget
├── screenshots/                 # acceptance-probe evidence (see EVIDENCE.md)
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── capstone.yaml
├── EVIDENCE.md
└── BUILDLOG.md
```

## Two ways to run

### Option A — Docker + PostgreSQL (matches the production-style stack)

```bash
cp .env.example .env
docker compose up --build
docker compose exec api python seed.py
```

### Option B — Local Python + SQLite (fastest for iterating; what this repo
was actually developed and tested against in a GitHub Codespace)

```bash
cp .env.example .env
# in .env, set:
#   DATABASE_URL=sqlite:///./widget_platform.db
pip install -r requirements.txt --break-system-packages
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

In a second terminal:
```bash
python3 seed.py
```

Note the printed `Widget ID` and `API Key` — you'll need both below.

`--reload` watches `.py` files only, **not** `.env`. After changing any
`GEO_PROVIDER_*_DOWN` or `EMAIL_SHOULD_FAIL` flag, restart the server for
the change to take effect.

## Try it interactively — Swagger UI

```
http://localhost:8000/docs
```

Click **Authorize** (top right) and paste your seeded API key to unlock the
authenticated endpoints (widget CRUD, dashboard). Public endpoints (`/config`,
`/widget.js`, `/submissions`) work without it.

## Try it end to end (cross-origin embed)

1. Put your seeded widget id into `test-site/index.html` in place of
   `WIDGET_ID`.
2. Serve that folder from a **different port**:
   ```bash
   cd test-site && python3 -m http.server 5500
   ```
3. Open the forwarded port-5500 URL — the widget renders, fetched
   cross-origin from the port-8000 API.
4. Submit the form, then check the dashboard:
   ```bash
   curl -H "X-API-Key: <your key>" \
        http://localhost:8000/dashboard/widgets/<widget id>/stats
   ```

## Proving the fallback chain / abuse controls (deterministic, no live network needed)

- Set `GEO_PROVIDER_A_DOWN=true` in `.env`, restart the server, submit with a
  spoofed `X-Forwarded-For` header (loopback IPs skip enrichment entirely) —
  geo still fills in via provider B.
- Set both `GEO_PROVIDER_A_DOWN=true` and `GEO_PROVIDER_B_DOWN=true` —
  submission still stores successfully, just without geo data.
- Set `EMAIL_SHOULD_FAIL=true` — submission still returns `201`.
- POST more than `RATE_LIMIT_PER_MINUTE` requests in a burst — you'll get
  `429` responses, and a normal request right after (once the window clears)
  still succeeds.
- Fill the hidden `website` field in a raw POST — request is rejected with
  `422`.

All of the above are captured as evidence in `EVIDENCE.md` and
`screenshots/`.

## Limitations (honest, per capstone scope)

- Auth is a static API key per tenant, not OAuth/JWT — sufficient for this
  capstone's contract, called out here rather than hidden.
- Rate limiting is in-memory/single-process — fine for one instance; a
  multi-worker deployment would need a shared store (Redis `INCR`+`EXPIRE`).
- Widget UI styling is intentionally minimal — the capstone is graded on the
  backend, not the CSS.
- Local development and testing were done against SQLite in a Codespace
  after the Postgres container hit a Docker bridge-network issue specific
  to that environment; the Postgres/Docker path in `docker-compose.yml` is
  unchanged and works the same way on a standard machine.