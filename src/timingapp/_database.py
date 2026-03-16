import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

DEFAULT_DB_PATH = (
    Path.home() / "Library/Application Support/info.eurocomp.Timing2/SQLite.db"
)


class ReadOnlyError(Exception):
    """Raised when a write operation is attempted on the read-only database."""


class Database:
    def __init__(self, path: Path = DEFAULT_DB_PATH) -> None:
        uri = f"file:{path}?mode=ro"
        self._engine = create_engine(
            "sqlite:///",
            creator=lambda: sqlite3.connect(uri, uri=True),
        )

        @event.listens_for(self._engine, "connect")
        def _set_query_only(conn: Any, _: Any) -> None:
            conn.execute("PRAGMA query_only = ON")

        self._Session = sessionmaker(
            bind=self._engine, autoflush=False
        )

        @event.listens_for(self._Session, "before_flush")
        def _block(_s: Any, _fc: Any, _i: Any) -> None:
            raise ReadOnlyError("read-only database")

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        with self._Session() as sess:
            yield sess
