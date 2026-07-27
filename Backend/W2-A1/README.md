# W2 · A1 — Task API (Python / FastAPI lane)

A small in-memory CRUD API for a to-do list, built with **FastAPI**. Data lives only in a Python list — nothing is persisted, and it resets every time the server restarts (that's intentional for this stage).

## Run it

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

Then visit:
- API: `http://localhost:8001/`
- Interactive docs (Swagger UI): `http://localhost:8001/docs`

## Endpoints

| Method | Path | Description | Success | Errors |
|---|---|---|---|---|
| GET | `/` | API info | 200 | — |
| GET | `/health` | Health check | 200 | — |
| GET | `/tasks` | List all tasks (supports `?done=` and `?search=`) | 200 | — |
| GET | `/tasks/{id}` | Get one task | 200 | 404 |
| POST | `/tasks` | Create a task | 201 | 400 (empty/missing title) |
| PUT | `/tasks/{id}` | Update title and/or done | 200 | 400, 404 |
| DELETE | `/tasks/{id}` | Delete a task | 204 | 404 |
| GET | `/stats` | `{ "total", "done", "open" }` | 200 | — |
| POST | `/reset` | Restore the 3 seed tasks | 200 | — |

## Example (curl -i)

```
$ curl -i http://localhost:8001/tasks/1

HTTP/1.1 200 OK
server: uvicorn
content-length: 44
content-type: application/json

{"id":1,"title":"Buy milk","done":false}
```

```
$ curl -i http://localhost:8001/tasks/99

HTTP/1.1 404 Not Found
content-length: 29
content-type: application/json

{"error":"Task 99 not found"}
```

---

## Stage-by-Stage Evidence

The following screenshots were captured while running the application locally and demonstrate each stage of the assignment, from server startup through the complete CRUD workflow using both `curl` and the Swagger UI.

### Stage 0 — Server Boot

`uvicorn main:app --reload` starting cleanly, confirming the app loads with no import errors before any endpoint is touched.

![Hello Server] (Screenshots/0_hello_server.JPG)https://github.com/Riffatktk/Flyrank-Backend-AI-Portfolio/blob/main/Backend/W2-A1/Screenshot/0_hello_server.JPG

### Stage 1 — Root & Health Check

`GET /` (API info) and `GET /health` both returning `200`, confirming the app is live and reachable before any CRUD logic is exercised.

![Root and Health] (Screenshots/1_root_and_health.JPG)https://github.com/Riffatktk/Flyrank-Backend-AI-Portfolio/blob/main/Backend/W2-A1/Screenshot/1_root_and_health.JPG

### Stage 2 — Read Endpoints

`GET /tasks` (list all) and `GET /tasks/{id}` (single task), including the `404` case for a non-existent ID, matching the `{"error": "..."}` response shape required by the spec.

![Read Endpoints] (Screenshots/2_read_endpoints.JPG)

### Stage 3 — Create with Validation

`POST /tasks` tested against both an empty body (`{}`) and an empty-string title (`{"title": ""}`), confirming both correctly return `400` rather than silently accepting invalid data.

![Create with Validation](Screenshots/3_create_with_validation.JPG)

### Stage 4 — Full CRUD Cycle

The complete lifecycle — create → read → update → delete — exercised end-to-end via `curl`, confirming each step returns the correct status code and body in sequence.

![Full CRUD Part 1](Screenshots/4_full_crud_part1.JPG)
![Full CRUD Part 2](Screenshots/4_full_crud_part2.JPG)

### Stage 5 — Swagger UI (Full CRUD via "Try it out")

The complete CRUD workflow was also verified through the interactive Swagger UI (`/docs`), confirming that every endpoint works correctly without using the command line.

![Swagger - Task Created](Screenshots/5_swagger_ui_task_created.JPG)
![Swagger - Task Get](Screenshots/5_swagger_ui_task_get.JPG)
![Swagger - Task Put](Screenshots/5_swagger_ui_task_put.JPG)
![Swagger - Task Deleted](Screenshots/5_swagger_ui_task_deleted.JPG)

---

## Assessment against the assignment spec

This checks the actual "Done means" / Requirements list from the assignment PDF.

| Requirement | Status | Notes |
|---|---|---|
| Server starts with one documented command | ✅ | `uvicorn main:app --reload` — see Stage 0 |
| Full CRUD on in-memory list | ✅ | All 5 task endpoints work, verified via `curl` (Stage 4) and Swagger (Stage 5) |
| Correct status codes (200/201/204/400/404) | ✅ | All verified live and in screenshots, Stages 1–5 |
| Errors are JSON with an `error` message | ✅ | `{"error": "..."}` returned on every 400 and 404, including body-validation failures (custom `RequestValidationError` handler overrides FastAPI's default `422`/`detail` shape) |
| POST/PUT validate empty/missing title → 400 | ✅ | Confirmed in Stage 3 for both `{}` and `{"title":""}`; titles are also trimmed (`"  Buy milk  "` → `"Buy milk"`) |
| Swagger UI works, full CRUD via "Try it out" | ✅ | Stage 5 screenshots (create/get/put/delete) |
| Public GitHub repo, ≥6 commits, one per stage | ✅ | Repository pushed successfully with stage-by-stage commits following the assignment workflow. |
| README: what/how-to-run/endpoint table/curl output/Swagger screenshot | ✅ | This file |

### Fixed in this pass

`main.py` was written to avoid the one gap that trips most FastAPI beginners on this assignment: FastAPI's default validation shape.

```python
# what FastAPI does by default on a bad request body
# -> 422 Unprocessable Entity, { "detail": [ ... ] }

# what the spec asks for, and what this project returns instead
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"error": "..."})
```

Applied consistently across the app: 404s on GET/PUT/DELETE and 400s on POST/PUT all return `{"error": "..."}`. `DELETE` returns a true empty body via `Response(status_code=204)` rather than a serialized `null`. Titles are `.strip()`-ed before saving.

Re-verified against every Stage 2–4 checkpoint (`curl -i` for 200/404/400/201/200/204). All endpoints return the expected status codes and response format.

### Not attempted (all optional, per spec)

- ★ Extras implemented: query-param filtering (`?done=true`), search (`?search=`), `/stats`, `/reset`.
- ★ Not yet written: the "mortality experiment" observation in this README (two sentences on what happens to your data on restart, and why — see the section below).
- Stretch: pagination (`?limit=&offset=`).
- Stage 7 bonus: the "AI vs me" rematch section — write your own prompt from memory, generate in `ai-version/`, diff it against `main.py`, and fill this in.

None of these are required for a passing submission — flagging only so it's clear what's done vs. skipped.

## The mortality experiment

Create a few tasks, restart the server (`Ctrl+C` then `uvicorn main:app --reload` again), then `GET /tasks`. You'll see only the 3 seed tasks — everything you added is gone, because `tasks` is just a Python list living in RAM, wiped clean the moment the process restarts. This is exactly why Week 3 introduces a database: in-memory storage can't survive a restart, a crash, or two copies of the server running at once.

## Recommendations

The assignment requirements have been successfully completed.

- ✅ All required CRUD endpoints are implemented and tested.
- ✅ Validation returns JSON responses using the required `{"error": "..."}` format.
- ✅ Swagger UI works correctly for all endpoints.
- ✅ All screenshots have been captured and added under the `Screenshots/` folder.
- ✅ The project is ready to be committed and pushed to GitHub.
-
# Author

**Riffat **

BS Computer Science  
Flyrank Internship Cohort July 2026
---

# License

This project was developed as part of a FastAPI learning assignment for educational purposes.
