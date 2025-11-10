"""Lightweight sentiment-analysis wrapper."""

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass
class SentimentResult:
    """Simple structure to hold model output."""

    label: str
    score: float
    payload: dict[str, Any]


class SentimentService:
    """Placeholder sentiment interface that will wrap HF pipelines."""

    def __init__(self, model_id: str) -> None:
        self.model_id = model_id

    def analyze(self, texts: Iterable[str]) -> list[SentimentResult]:
        """Perform sentiment analysis (stubbed)."""

        return [
            SentimentResult(label="neutral", score=0.0, payload={"text": text})
            for text in texts
        ]
