from pathlib import Path as FilePath

from timingapp._database import DEFAULT_DB_PATH, Database, ReadOnlyError
from timingapp.models import (
    AppActivity,
    AppActivityWithStrings,
    Application,
    Device,
    Event,
    EventSource,
    EventSourceTaskActivity,
    Filter,
    Integration,
    IntegrationLogResult,
    IntegrationProject,
    Path,
    Project,
    TaskActivity,
    Title,
)

__all__ = [
    "DEFAULT_DB_PATH",
    "Database",
    "ReadOnlyError",
    "open_database",
    "get_database",
    "AppActivity",
    "AppActivityWithStrings",
    "Application",
    "Device",
    "Event",
    "EventSource",
    "EventSourceTaskActivity",
    "Filter",
    "Integration",
    "IntegrationLogResult",
    "IntegrationProject",
    "Path",
    "Project",
    "TaskActivity",
    "Title",
]

_db: Database | None = None


def open_database(path: FilePath = DEFAULT_DB_PATH) -> Database:
    """Open and cache a Database connection. Returns the Database instance."""
    global _db
    _db = Database(path)
    return _db


def get_database() -> Database:
    """Return the cached Database. Raises RuntimeError if not yet opened."""
    if _db is None:
        raise RuntimeError(
            "No database opened. Call open_database() first."
        )
    return _db
