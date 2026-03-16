import json
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Float, Text
from sqlalchemy.engine import Dialect
from sqlalchemy.types import TypeDecorator


class UnixTimestamp(TypeDecorator[datetime]):
    """Converts Unix float timestamps to UTC datetime objects."""

    impl = Float
    cache_ok = True

    def process_result_value(
        self, value: Any, dialect: Dialect
    ) -> datetime | None:
        if value is None:
            return None
        return datetime.fromtimestamp(float(value), tz=timezone.utc)

    def process_bind_param(self, value: Any, dialect: Dialect) -> float | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.timestamp()
        return float(value)


class JSONText(TypeDecorator[Any]):
    """Converts JSON text columns to Python dicts/lists."""

    impl = Text
    cache_ok = True

    def process_result_value(
        self, value: Any, dialect: Dialect
    ) -> Any:
        if value is None:
            return None
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value  # Return raw string on parse error (matches Ruby behavior)

    def process_bind_param(self, value: Any, dialect: Dialect) -> str | None:
        if value is None:
            return None
        if isinstance(value, str):
            return value
        return json.dumps(value)
