# EVIDENCE.md

One pasted proof per checkbox in the capstone brief's Requirements section.
Fill each one in as you build — claims without evidence score as not done.

## Widget management

- [ ] Authenticated CRUD endpoints for widgets; requests without valid auth are rejected.
  <!-- paste: curl to POST/GET/PUT/DELETE without X-API-Key -> 401 -->

- [ ] Multi-tenant isolation proven: tenant A cannot read or modify tenant B's widgets or submissions.
  <!-- paste: two seeded tenants, tenant B's key used against tenant A's widget id -> 404 -->

## Widget delivery

- [ ] Embed snippet generated per widget.
  <!-- paste: response body from POST /widgets showing embed_snippet -->

- [ ] Public config endpoint serves a small payload with correct HTTP cache headers.
  <!-- paste: curl -I showing Cache-Control: public, max-age=60 -->

- [ ] Widget JavaScript is served as a versioned bundle (new version = new URL or cache-bust).
  <!-- paste: curl -I on /widget.js showing Cache-Control: public, max-age=31536000, immutable -->

- [ ] The widget renders on a page served from a different origin than your API.
  <!-- paste: screenshot description / confirmation from test-site page -->

## Public submission API

- [ ] Cross-origin submissions work: CORS headers correct, preflight (OPTIONS) handled.
  <!-- paste: curl -X OPTIONS showing Access-Control-Allow-Origin -->

- [ ] All incoming input validated; malformed and oversized payloads rejected with appropriate 4xx codes and JSON errors.
  <!-- paste: curl with empty/oversized data -> 422 with error body -->

- [ ] Valid submissions stored safely, linked to the right widget and tenant.
  <!-- paste: successful POST + matching GET from dashboard -->

## Abuse protection

- [ ] Rate limiting per IP and/or per widget returns 429 under a burst — and the API keeps serving legitimate traffic.
  <!-- paste: loop of curls, last few showing 429, next request after cooldown -> 201 -->

- [ ] At least one spam-prevention technique (honeypot field, token, or heuristic) demonstrably blocks a spam submission.
  <!-- paste: curl with website field filled -> 422 -->

## Enrichment & safe side effects

- [ ] IP→geo enrichment uses a provider fallback chain: provider A down → provider B answers → submission enriched.
  <!-- paste: GEO_PROVIDER_A_DOWN=true, submission still shows country/city, geo_provider=ipapi.co -->

- [ ] All providers down → submission still succeeds (without geo). Degrade, never fail.
  <!-- paste: both flags true, submission -> 201, country/city null -->

- [ ] A failing confirmation email / webhook does not prevent the submission from being stored.
  <!-- paste: EMAIL_SHOULD_FAIL=true, submission -> 201 -->

## Documentation

- [ ] README with architecture diagram, setup instructions, and API documentation; the required files from Section 11 present.
  <!-- paste: file listing of repo root -->
