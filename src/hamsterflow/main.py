"""ASGI entry point for HamsterFlow."""

from fastapi import FastAPI

from hamsterflow import get_settings
from hamsterflow.api import router as api_router
from hamsterflow.storage import Database


def create_application() -> FastAPI:
    """Construct the FastAPI application."""

    settings = get_settings()
    db = Database(url=settings.database_url)
    db.connect()

    app = FastAPI(title="HamsterFlow", version="2025.0.0")
    app.include_router(api_router)
    return app


app = create_application()
