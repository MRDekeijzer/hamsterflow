"""Placeholder persistence layer that will wrap SQLModel."""

from dataclasses import dataclass


@dataclass
class Database:
    """Very small shim around the future SQLModel session factory."""

    url: str

    def connect(self) -> None:
        """Create tables and warm up the connection (stub)."""

        # TODO: swap with SQLModel engine + metadata.create_all
        return None
