import json
import sqlite3
import time
from pathlib import Path
from typing import Any

from app.core.config import get_settings


def _db_path() -> Path:
    database_url = get_settings().database_url
    if not database_url.startswith("sqlite:///"):
        raise ValueError("Phase 1 cache expects a sqlite:/// DATABASE_URL")
    return Path(database_url.replace("sqlite:///", "", 1))


class CacheStore:
    def __init__(self) -> None:
        self.path = _db_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _init_db(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS api_cache (
                    cache_key TEXT PRIMARY KEY,
                    payload TEXT NOT NULL,
                    expires_at INTEGER NOT NULL
                )
                """
            )

    def get(self, key: str) -> Any | None:
        now = int(time.time())
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload, expires_at FROM api_cache WHERE cache_key = ?",
                (key,),
            ).fetchone()
        if row is None:
            return None
        payload, expires_at = row
        if expires_at < now:
            self.delete(key)
            return None
        return json.loads(payload)

    def set(self, key: str, payload: Any, ttl_seconds: int) -> None:
        expires_at = int(time.time()) + ttl_seconds
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO api_cache(cache_key, payload, expires_at)
                VALUES (?, ?, ?)
                ON CONFLICT(cache_key) DO UPDATE SET
                    payload = excluded.payload,
                    expires_at = excluded.expires_at
                """,
                (key, json.dumps(payload), expires_at),
            )

    def delete(self, key: str) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM api_cache WHERE cache_key = ?", (key,))
