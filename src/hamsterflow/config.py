"""Application settings powered by Pydantic."""

from functools import lru_cache
from typing import Any

from pydantic import AnyHttpUrl, BaseModel, Field
from pydantic_settings import BaseSettings


class SchedulerSettings(BaseModel):
    """Knobs that control the in-process scheduler."""

    pull_interval_minutes: int = Field(
        default=30,
        ge=1,
        description="Number of minutes between RSS ingestion jobs.",
    )


class AppSettings(BaseSettings):
    """Top-level settings for the HamsterFlow service."""

    rss_feeds: list[AnyHttpUrl] = Field(
        default_factory=lambda: ["https://feeds.feedburner.com/TechCrunch/"],
        description="List of RSS feeds to ingest on a schedule.",
    )
    database_url: str = Field(
        default="jdbc:sqlite:C:Users\\Harvest\\hamsterflow.db",
        description="SQLModel-compatible database URL.",
    )
    sentiment_model: str = Field(
        default="distilbert-base-uncased-finetuned-sst-2-english",
        description="Hugging Face model id used for sentiment analysis.",
    )
    scheduler: SchedulerSettings = Field(
        default_factory=SchedulerSettings,
        description="Settings that configure the local scheduler.",
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    def dump_debug(self) -> dict[str, Any]:
        """Return a redacted dict suitable for logging."""
        data = self.model_dump()
        # Hide secrets when we introduce them later.
        return data


@lru_cache(1)
def get_settings() -> AppSettings:
    """Return a cached settings instance."""
    return AppSettings()
