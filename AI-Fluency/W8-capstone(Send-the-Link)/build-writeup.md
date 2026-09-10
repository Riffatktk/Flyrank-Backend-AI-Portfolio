# Build write-up

## Stack, and why

FastAPI was a better fit because I was building APIs, not a full web
application. Compared to Django, I didn't need a full framework with a
lot of built-in features for a project this focused. FastAPI's
automatic Swagger docs, Pydantic validation, and Python type hints made
development and testing easier than Flask would have.

## The hardest thing that broke

In ninja-grid, I had a Git merge/recovery issue where some Category and
Unit files were lost or conflicted after merging upstream changes. I
first checked the Git history and repository status, then restored the
missing Clean Architecture layers — models, repositories, schemas, and
services — and verified the project with `compileall`. That taught me
to use Git history and small verification steps instead of trying to
fix everything at once.

## What I'd build next

The Category & Unit Master Data Management Module for the ninja-grid-backend
Pharmacy POS project (issue #4): CRUD endpoints under `/api/v1/categories`
and `/api/v1/units`, service/repository layer, tenant-scoped, currently
in PR review.

## Plan to keep building

Every completed piece gets added to `case-studies/cases.js` as a
three-beat entry (problem / what I did / what came of it) — see
`case-studies/HOW-TO-ADD-A-CASE.md`. Reminder set for the day the
Category & Unit module PR merges.q