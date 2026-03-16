import sqlite3
from pathlib import Path

import pytest

from timingapp._database import Database, ReadOnlyError
from timingapp import open_database, get_database


class TestDatabase:
    def test_session_context_manager(self, db: Database):
        with db.session() as sess:
            assert sess is not None

    def test_read_only_error_on_flush(self, synthetic_db: Path):
        from timingapp._base import TimingBase
        db = Database(synthetic_db)
        with db.session() as sess:
            # Begin a transaction to allow flush attempt
            sess.begin()
            from timingapp.models.title import Title
            obj = Title(id=999, stringValue="test")
            sess.add(obj)
            with pytest.raises(ReadOnlyError):
                sess.flush()

    def test_get_database_raises_if_not_opened(self, monkeypatch):
        import timingapp
        monkeypatch.setattr(timingapp, "_db", None)
        with pytest.raises(RuntimeError, match="No database opened"):
            get_database()

    def test_open_database_returns_database(self, synthetic_db: Path):
        db = open_database(synthetic_db)
        assert isinstance(db, Database)

    def test_get_database_after_open(self, synthetic_db: Path):
        open_database(synthetic_db)
        db = get_database()
        assert isinstance(db, Database)

    def test_query_only_pragma(self, synthetic_db: Path):
        db = Database(synthetic_db)
        with db.session() as sess:
            result = sess.execute(
                __import__("sqlalchemy").text("PRAGMA query_only")
            ).scalar()
            assert result == 1
