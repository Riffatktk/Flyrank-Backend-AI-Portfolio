/**
 * cases.js — the ONLY file you touch to add a new case study.
 *
 * How to add the next one:
 *   1. Copy the block below (between the { and the },).
 *   2. Paste it as a new entry at the TOP of the CASES array (newest first).
 *   3. Bump the id to the next case_0XX number.
 *   4. Fill in the three beats: problem, action, result. One or two
 *      sentences each — the same shape you used in Week 2.
 *   5. Save. case-studies.html reads this file automatically, nothing
 *      else needs to change.
 *
 * Full walkthrough: see HOW-TO-ADD-A-CASE.md in this same folder.
 */

const CASES = [
  {
    id: "case_003",
    title: "Category & Unit Master Data Module — Pharmacy POS",
    date: "2026-09",
    stack: ["FastAPI", "Async SQLAlchemy", "PostgreSQL", "Pydantic"],
    // beat 1 — the problem
    problem:
      "A multi-tenant pharmacy POS needed a clean, tenant-scoped way to " +
      "manage product categories and units of measure before any inventory " +
      "work could start.",
    // beat 2 — what you did
    action:
      "Built the CRUD service and repository layer for /api/v1/categories " +
      "and /api/v1/units inside an existing Clean Architecture codebase, " +
      "enforcing tenant_id isolation and validating input with Pydantic " +
      "schemas, then opened a PR against the team's fork-and-branch workflow.",
    // beat 3 — what came of it
    result:
      "PLACEHOLDER — fill this in once the PR is reviewed: what shipped, " +
      "what the reviewer said, what you'd do differently next time.",
    links: {
      repo: "https://github.com/Riffatktk/ninja-grid-backend",
      writeup: ""
    }
  },
  {
    id: "case_002",
    title: "The Polite Scraper — Books to Scrape",
    date: "2026-08",
    stack: ["Python", "requests", "BeautifulSoup", "Pydantic"],
    problem:
      "Needed a scraper that behaves like a good citizen of the web, not " +
      "just one that extracts data — checking robots.txt, validating " +
      "every record, and failing loudly instead of silently.",
    action:
      "Wrote a Books to Scrape crawler that checks robots.txt before " +
      "touching a page, parses listings into Pydantic models so bad data " +
      "can't slip through, and ships with an offline test suite instead " +
      "of hitting the live site on every run.",
    result:
      "All 7 offline parser tests pass; the scraper produces clean, " +
      "schema-validated JSON and documents the robots.txt check as a " +
      "deliberate design decision, not an afterthought.",
    links: {
      repo: "https://github.com/Riffatktk/Flyrank-Backend-AI-Portfolio",
      writeup: ""
    }
  },
  {
    id: "case_001",
    title: "Dockerized FastAPI + PostgreSQL, Repository Pattern",
    date: "2026-07",
    stack: ["FastAPI", "PostgreSQL", "Docker", "Repository Pattern"],
    problem:
      "A minimal FastAPI app is easy to demo and hard to trust — it needed " +
      "a real database, a layer that keeps SQL out of the route handlers, " +
      "and a setup someone else could run with one command.",
    action:
      "Containerized the app with Docker Compose (API + Postgres), and " +
      "restructured data access behind a repository layer so the service " +
      "logic never talks to SQL directly.",
    result:
      "Anyone can clone the repo and be running against a real database " +
      "in one `docker compose up`; the repository pattern made the next " +
      "feature (background jobs) a clean add rather than a rewrite.",
    links: {
      repo: "https://github.com/Riffatktk/Flyrank-Backend-AI-Portfolio",
      writeup: ""
    }
  }
];