# How I built my portfolio with AI

I set out to build a backend-focused developer portfolio that proves I
can take a problem from spec to a working, tested system — not just
list technologies. The centerpiece is a set of real case studies: a
Dockerized FastAPI + PostgreSQL service, a polite web scraper, and CRUD
work on a multi-tenant pharmacy POS.

Claude's biggest win was on the ninja-grid Category and Unit CRUD
recovery. After a Git merge conflict left some Clean Architecture files
missing, Claude helped me map where the models, repositories, schemas,
and services belonged and how the pieces connected — which saved a lot
of time. I still had to apply the changes, run the project, and verify
everything worked myself.

The hardest real break was in my A9 scraper: early on, a single failed
page could crash the whole pipeline instead of just that one book. I
added proper error handling so failures get recorded and the scraper
keeps going, plus Pydantic validation so the final data stays
consistent. The lesson: a production-style scraper can't assume every
request succeeds.

My honest limitation is that I still need more experience designing
larger systems independently. I can build APIs, work with databases,
Git, and Docker, but complex, multi-component problems still need
guidance sometimes. I use AI as a development assistant, not a
replacement for understanding my own code — I verify everything by
running and testing it. I'm comfortable being stuck and learning
whatever the problem needs.

---

*Posted as part of the FlyRank AI Fluency Internship capstone.*