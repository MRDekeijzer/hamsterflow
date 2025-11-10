By @MRDekeijzer

### Project goal
**Goal (SMART, 8 hours):**
Deliver a Dockerized local FastAPI service that ingests RSS feeds on a schedule, extracts article text with trafilatura, performs offline sentiment via a Hugging Face Transformers pipeline after first model download, stores results in SQLite via SQLModel, and exposes filterable query + simple stats endpoints. “Done” when all acceptance tests pass on a clean machine with no internet after the first run completes the model download and initial ingest.

**Scope**

* Inputs: list of RSS URLs (env or `config.toml`).
* Processing: periodic pull (APScheduler), fetch + parse RSS, deduplicate by URL+hash, fetch article HTML, extract with trafilatura, run HF sentiment pipeline (cpu), persist.
* API: `/health`, `/articles` (filters: date range, source, sentiment, keyword), `/stats` (counts by day, by source, sentiment distribution), `/feeds/reload` (manual trigger).
* Persistence: SQLite file `data/app.db`.
* Offline mode: after first run, service and inference work without internet.

**Time-boxed plan (8 hours total)**

1. **H0–H1: Project skeleton + env**

* Create repo layout: `app/` (api, models, jobs, db, utils), `tests/`, `Dockerfile`, `pyproject.toml`, `config.example.toml`, `Makefile`, `README.md`.
* Pin libs: `fastapi`, `uvicorn[standard]`, `sqlmodel`, `trafilatura`, `feedparser`, `apscheduler`, `transformers`, `torch` (cpu), `pydantic-settings`, `python-dotenv`, `orjson`, `httpx`, `uvloop` (Linux), `pytest`, `pytest-asyncio`.

2. **H1–H2: Data model + DB**

* Define `Article` (id, url, source, title, published_at, text, sentiment_label, sentiment_score, created_at, updated_at, url_hash).
* SQLModel engine, session dependency, migrations-by-recreate on startup for MVP.
* Implement dedup on `url_hash` unique index.

3. **H2–H3: RSS ingest pipeline**

* `fetch_feeds()` reads RSS list, parses with `feedparser`, normalizes fields, enqueues URLs for extraction.
* `extract_and_analyze(url)` uses `httpx` and `trafilatura` to get clean text; simple heuristic fallback if empty.
* HF `pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")` cached to `~/.cache/huggingface` inside container volume `/models`.
* Persist records with upsert by `url_hash`.

4. **H3–H4: Scheduler + settings**

* `APScheduler` background job every 15 min.
* Settings via `BaseSettings` with `.env` + `config.toml` path override.
* Health checks for model loaded, DB reachable, last job status.

5. **H4–H5: API endpoints**

* `/articles`: pagination, filters: `q`, `source`, `sentiment=positive|negative|neutral?`, `date_from`, `date_to`.
* `/stats`: totals, by sentiment, by source, daily counts last 30 days.
* `/feeds/reload`: trigger immediate ingest.
* JSON via orjson; Pydantic response models.

6. **H5–H6: Docker + offline flow**

* Multi-stage Dockerfile. Stage 1 installs deps and downloads model via a build or first-run hook.
* Runtime mounts `/models` and `data/`.
* Make targets: `make build`, `make run`, `make test`, `make ingest`.
* Document “first run online, subsequent offline” and how to preload models: `python -c "from transformers import pipeline; pipeline('sentiment-analysis')"`.

7. **H6–H7: Tests + validation**

* Unit tests: RSS parser, extractor stub, dedup logic, sentiment wrapper.
* API tests: filters and stats with seeded fixtures.
* Smoke test script to run once online, then stop network and re-run API + inference.

8. **H7–H8: Polish + acceptance**

* Logging, error handling, graceful shutdown.
* README with setup, env vars, endpoints, curl examples, offline checklist.
* Verify acceptance criteria on a clean container.

**Acceptance criteria**

* Start: `docker compose up` exposes FastAPI on `localhost:8000` with `/docs`.
* First run online pulls model and ingests at least one feed item; subsequent restarts with no network still respond with sentiment for already-stored items and accept new HTML files via local path fallback (documented).
* `/articles` returns filtered results correctly; `/stats` returns counts with deterministic test fixtures.
* Scheduler runs automatically and logs last run.
* DB file persists on volume.
* All tests pass: `pytest -q` green.
* Container image size ≤ 2.5 GB (CPU PyTorch + transformers).
* No duplicate articles for identical URLs.

**Assumptions**

* English sentiment is acceptable; neutral derived by thresholding if using binary model.
* Feeds provide `link`, `title`, `published_parsed`.
* CPU only; no GPU stack.
* Offline mode excludes fetching new web pages; system continues to serve and analyze any locally provided HTML if added.