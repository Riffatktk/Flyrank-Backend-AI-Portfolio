# BUILDLOG.md

Honest AI-usage log. Where AI helped, where it was wrong, what I changed.

## Session 1 — 2026-09-10 to 2026-09-13

**What I asked AI for:**

I used AI mainly to help me scaffold the FastAPI capstone project and think through the overall structure. This included the Tenant, Widget, and Submission models, authentication dependency, widget CRUD routes, the public submission endpoint, CORS, rate limiting, honeypot protection, the geo-provider fallback service, email side effects, dashboard aggregation, Docker setup, and the initial test suite.

I did not treat the generated code as final. I ran the project myself, checked the behavior through Swagger/curl, and changed parts that did not work correctly in my environment.

**What it got right:**

The basic project structure and most of the application flow worked well as a starting point. The Tenant/Widget/Submission models, CRUD structure, request validation, and the general separation into routers, services, and dependencies were useful and mostly worked as expected.

The public submission flow also gave me a good starting point for adding the rate limiter, honeypot check, geo fallback logic, and email side-effect handling. The test structure was also helpful because it gave me specific behaviors to verify instead of only checking whether the API started successfully.

**What it got wrong / what I changed (and why):**

1. **Auth returned 422 instead of 401 for a missing API key**

   The first authentication implementation used `Header(...)`. Because the header was required at the FastAPI validation level, a missing `X-API-Key` caused a 422 validation error before my authentication code could handle it.

   I changed `auth.py` to use `APIKeyHeader` with `auto_error=False` and then handled the missing key myself. This allowed me to return the expected 401 response. It also gave me the `Authorize` button in Swagger UI, which made testing the protected endpoints much easier.

2. **Docker + Postgres networking failed in my Codespace**

   The Docker setup worked differently in my Codespace than I expected. The Postgres container could be healthy, but the API container was still timing out when trying to connect to the database.

   I checked the containers and their status instead of assuming the application code was broken. Since the problem was related to the Docker/Codespace networking environment, I focused on getting the application working and verifying the API behavior separately rather than changing database logic just to hide an environment-specific problem.

3. **The pinned requirements did not install correctly on Python 3.14**

   My Codespace was running Python 3.14. Some of the originally pinned dependency versions did not have compatible prebuilt wheels. In particular, `pydantic-core` tried to compile from source using Rust/PyO3, which caused installation problems.

   I removed the overly strict version pins so pip could select compatible package versions with available wheels. After that, the dependencies installed successfully in my environment.

4. **`.env` changes were not picked up automatically**

   I initially expected `uvicorn --reload` to notice changes in `.env`, but reload was watching the Python source files rather than environment-variable changes.

   Because of this, when I changed settings such as `GEO_PROVIDER_A_DOWN`, I had to restart the server manually before testing again. I now restart Uvicorn explicitly after changing `.env` values so I know the new configuration is actually being used.

**What I tested/verified myself (not just accepted):**

I tested the main acceptance behavior myself using Swagger UI and API requests.

I checked authentication failures and successful authenticated requests, widget CRUD behavior, tenant isolation, and the public submission endpoint. I also tested the rate-limiting behavior and the honeypot field instead of only checking that the code existed.

For the geo service, I changed the provider environment flags and checked that the fallback chain moved to the next available provider when one was disabled.

I also tested the email side-effect failure case to make sure an email problem did not prevent the submission itself from being processed.

I checked the API responses and status codes manually and used the test suite to catch regressions after making changes. I kept the important results/screenshots in `EVIDENCE.md` so the final behavior is backed by actual tests rather than just generated code.

**What I can explain about my own code:**

One example is the authentication code. I understand why `APIKeyHeader(auto_error=False)` is used: I want the request to reach my own authentication function even when the API key is missing, so I can return a proper 401 instead of FastAPI returning a 422 automatically.

Another example is the public submission flow. The honeypot field is a hidden field intended for bots. If that field is filled, the request is rejected instead of being treated like a normal submission. The rate limiter is also there to stop repeated public requests from being abused.

I can also explain the geo fallback service. The idea is not to depend on one provider. If the first provider is unavailable or disabled, the service tries the next provider in the configured fallback chain. This is why the provider flags are useful during testing.

For the email side effect, I kept it separate from the main submission logic because an email failure should not make the actual form submission fail. The submission is the main operation; sending the notification is a side effect that can fail independently.