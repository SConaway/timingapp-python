import json
from datetime import datetime, timezone

import pytest

from timingapp._types import JSONText, UnixTimestamp


class TestUnixTimestamp:
    def test_none_returns_none(self):
        ts = UnixTimestamp()
        result = ts.process_result_value(None, None)
        assert result is None

    def test_converts_to_utc_datetime(self):
        ts = UnixTimestamp()
        result = ts.process_result_value(1700000000.0, None)
        assert isinstance(result, datetime)
        assert result.tzinfo == timezone.utc

    def test_known_timestamp(self):
        ts = UnixTimestamp()
        result = ts.process_result_value(0.0, None)
        assert result == datetime(1970, 1, 1, tzinfo=timezone.utc)

    def test_bind_param_none(self):
        ts = UnixTimestamp()
        assert ts.process_bind_param(None, None) is None

    def test_bind_param_datetime(self):
        ts = UnixTimestamp()
        dt = datetime(1970, 1, 1, tzinfo=timezone.utc)
        result = ts.process_bind_param(dt, None)
        assert result == 0.0

    def test_bind_param_float(self):
        ts = UnixTimestamp()
        result = ts.process_bind_param(1700000000.0, None)
        assert result == 1700000000.0


class TestJSONText:
    def test_none_returns_none(self):
        jt = JSONText()
        assert jt.process_result_value(None, None) is None

    def test_parses_dict(self):
        jt = JSONText()
        result = jt.process_result_value('{"key": "value"}', None)
        assert result == {"key": "value"}

    def test_parses_list(self):
        jt = JSONText()
        result = jt.process_result_value('[1, 2, 3]', None)
        assert result == [1, 2, 3]

    def test_fallback_on_invalid_json(self):
        jt = JSONText()
        result = jt.process_result_value("not-json", None)
        assert result == "not-json"

    def test_bind_param_none(self):
        jt = JSONText()
        assert jt.process_bind_param(None, None) is None

    def test_bind_param_dict(self):
        jt = JSONText()
        result = jt.process_bind_param({"a": 1}, None)
        assert json.loads(result) == {"a": 1}

    def test_bind_param_string_passthrough(self):
        jt = JSONText()
        result = jt.process_bind_param('{"a": 1}', None)
        assert result == '{"a": 1}'
