import pytest
from sqlalchemy import select

from timingapp._database import Database
from timingapp.models.title import Title
from timingapp.models.path import Path
from timingapp.models.application import Application
from timingapp.models.device import Device
from timingapp.models.filter import Filter
from timingapp.models.integration import Integration
from timingapp.models.integration_log_result import IntegrationLogResult


class TestTitle:
    def test_query_all(self, db: Database):
        with db.session() as sess:
            titles = sess.scalars(select(Title)).all()
            assert len(titles) >= 2

    def test_string_value(self, db: Database):
        with db.session() as sess:
            title = sess.get(Title, 1)
            assert title is not None
            assert title.stringValue == "Google - Safari"


class TestPath:
    def test_query_all(self, db: Database):
        with db.session() as sess:
            paths = sess.scalars(select(Path)).all()
            assert len(paths) >= 2

    def test_string_value(self, db: Database):
        with db.session() as sess:
            path = sess.get(Path, 1)
            assert path is not None
            assert path.stringValue == "/Applications/Safari.app"


class TestApplication:
    def test_query_all(self, db: Database):
        with db.session() as sess:
            apps = sess.scalars(select(Application)).all()
            assert len(apps) >= 2

    def test_bundle_identifier(self, db: Database):
        with db.session() as sess:
            app = sess.get(Application, 1)
            assert app is not None
            assert app.bundleIdentifier == "com.apple.Safari"


class TestDevice:
    def test_query_all(self, db: Database):
        with db.session() as sess:
            devices = sess.scalars(select(Device)).all()
            assert len(devices) >= 2

    def test_primary_key_is_local_id(self, db: Database):
        with db.session() as sess:
            device = sess.get(Device, 1)
            assert device is not None
            assert device.name == "MacBook Pro"

    def test_non_local_device(self, db: Database):
        with db.session() as sess:
            device = sess.get(Device, 2)
            assert device is not None
            assert device.local_device == 0


class TestFilter:
    def test_query_all(self, db: Database):
        with db.session() as sess:
            filters = sess.scalars(select(Filter)).all()
            assert len(filters) >= 3

    def test_samples_scope(self, db: Database):
        with db.session() as sess:
            samples = sess.scalars(Filter.samples()).all()
            assert len(samples) == 1
            assert samples[0].name == "Sample Filter"

    def test_self_referential_parent(self, db: Database):
        with db.session() as sess:
            child = sess.get(Filter, 3)
            assert child is not None
            assert child.parent is not None
            assert child.parent.id == 1

    def test_children_relationship(self, db: Database):
        with db.session() as sess:
            parent = sess.get(Filter, 1)
            assert parent is not None
            assert len(parent.children) == 1
            assert parent.children[0].id == 3


class TestIntegration:
    def test_query(self, db: Database):
        with db.session() as sess:
            integrations = sess.scalars(select(Integration)).all()
            assert len(integrations) >= 1
            assert integrations[0].name == "Jira"


class TestIntegrationLogResult:
    def test_query(self, db: Database):
        with db.session() as sess:
            from datetime import timezone
            results = sess.scalars(select(IntegrationLogResult)).all()
            assert len(results) >= 1
            result = results[0]
            assert result.result == "success"
            assert result.details == {"items": 5}
            assert result.timestamp is not None
            assert result.timestamp.tzinfo == timezone.utc
