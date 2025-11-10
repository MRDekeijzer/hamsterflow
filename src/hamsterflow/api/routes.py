"""FastAPI routes exposed by the service."""

from fastapi import APIRouter

from hamsterflow.config import get_settings

router = APIRouter()


@router.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    """Simple readiness indicator for orchestration layers."""
    settings = get_settings()
    return {
        "status": "ok",
        "feeds_configured": str(len(settings.rss_feeds)),
    }
