# HamsterFlow Instructions

## Overview
HamsterFlow was bootstrapped as a layered FastAPI project that will ingest RSS feeds, extract article text, score sentiment offline, and expose results via HTTP and CLI workflows. The current codebase wires together the skeleton pieces so you can run the API/CLI, extend each layer independently, and add real implementations incrementally.

## Code Layout
- `src/hamsterflow/config.py` – Pydantic settings (`AppSettings`) with defaults for the TechCrunch feed, DB URL, sentiment model, and scheduler knobs. Values can be overridden via `.env` or env vars.
- `src/hamsterflow/main.py` – FastAPI factory that loads settings, prepares the placeholder DB adapter, and mounts the API router.
- `src/hamsterflow/api/routes.py` – All HTTP endpoints (currently just `/health`) live here. Additional routers should be added in this module or subpackages.
- `src/hamsterflow/ingest/` – RSS ingestion stubs (`fetch_and_extract`) that will evolve into feedparser + trafilatura integration.
- `src/hamsterflow/analysis/` – Sentiment interface placeholder meant to wrap a Hugging Face pipeline.
- `src/hamsterflow/storage/` – Future SQLModel-backed persistence layer; today only exposes a `Database` shim.
- `src/hamsterflow/__main__.py` – CLI entry point (`python -m hamsterflow ...`) for running maintenance/ingestion commands.
- `tests/unit` & `tests/integration` – Pytest suites that mirror the runtime layout. Unit tests already cover settings and the API healthcheck; integration tests are scaffolded but skipped.

## Execution Flow
1. **Settings** – Every entry point calls `get_settings()`, returning a cached `AppSettings` instance (Pydantic auto-loads from `.env`).
2. **Application startup** – `create_application()` in `main.py` initializes settings, instantiates the `Database` shim (future home for SQLModel engine creation), and constructs the FastAPI app.
3. **Routing** – The FastAPI app mounts `api.router`. Requests hit the router modules; dependencies will eventually use the ingest, storage, and analysis subpackages.
4. **CLI** – `python -m hamsterflow --dry-run` shares the same settings, calls the ingestion stub, and will later persist or print outputs.
5. **Testing** – `pytest` imports from the installed editable package (`uv pip install -e .`), exercising whichever layer you target.

## Running & Debugging
1. Ensure the venv is active (`.\.venv\Scripts\Activate.ps1`).
2. Install the project editable so imports resolve: `uv pip install -e .`.
3. Launch the API: `uvicorn hamsterflow.main:app --reload`. Hit `GET /health` to verify readiness.
4. Run the CLI ingestion dry-run: `uv run python -m hamsterflow --dry-run`.
5. Execute tests: `uv run pytest` (or pick a specific module, e.g., `uv run pytest tests/unit/test_app.py -vv`).
6. Use IDE debuggers by pointing them at the module (`hamsterflow.main`) or script (`python -m hamsterflow`)—the cached settings ensure consistent behavior between runs.

## Future Steps Toward Full Functionality
1. **RSS ingestion** – Implement `fetch_and_extract` using `feedparser` + `trafilatura`, normalize article metadata, and handle deduplication.
2. **Persistence** – Replace `storage.Database` with SQLModel models (feeds, articles, sentiment scores) backed by SQLite; expose session helpers for API/tests.
3. **Scheduler** – Integrate APScheduler (or FastAPI background tasks) to run the ingest job at `scheduler.pull_interval_minutes`, wiring job status logging.
4. **Sentiment pipeline** – Build `SentimentService` on top of a Hugging Face Transformers pipeline, cache the model locally, and provide batching utilities.
5. **API endpoints** – Add routes for listing articles, filtering by feed/date/sentiment, and returning simple stats (counts, averages).
6. **CLI enhancements** – Extend the CLI to trigger on-demand ingests, export data, and inspect scheduler state.
7. **Tests & CI** – Add unit/integration tests for ingestion, storage, and API filtering. Wire a GitHub Actions workflow (formatting, pytest) plus fixtures for temporary SQLite DBs.
8. **Docker packaging** – Produce a Dockerfile that installs dependencies, pre-downloads the sentiment model, and configures a healthcheck for deployment.
9. **Config secrets** – Once external services or model tokens are needed, add secure settings/redaction logic (the `dump_debug` method is ready for this).

Work through the list sequentially (ingest → storage → sentiment → API) to keep the implementation manageable and testable at each stage.
