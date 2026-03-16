from sqlalchemy import select

from timingapp._database import Database
from timingapp.models.event import Event
from timingapp.models.event_source import EventSource
from timingapp.models.event_source_task_activity import EventSourceTaskActivity
from timingapp.models.integration_project import IntegrationProject


class TestEventSource:
    def test_templates_scope(self, db: Database):
        with db.session() as sess:
            templates = sess.scalars(EventSource.templates()).all()
            assert len(templates) == 1
            assert templates[0].title == "Template Source"

    def test_favorites_scope(self, db: Database):
        with db.session() as sess:
            favorites = sess.scalars(EventSource.favorites()).all()
            assert len(favorites) == 1
            assert favorites[0].title == "Favorite Source"

    def test_template_relationship(self, db: Database):
        with db.session() as sess:
            source = sess.get(EventSource, 2)
            assert source is not None
            assert source.template is not None
            assert source.template.id == 1

    def test_instances_relationship(self, db: Database):
        with db.session() as sess:
            template = sess.get(EventSource, 1)
            assert template is not None
            assert len(template.instances) == 1
            assert template.instances[0].id == 2


class TestEvent:
    def test_query(self, db: Database):
        with db.session() as sess:
            events = sess.scalars(select(Event)).all()
            assert len(events) == 1

    def test_timestamps_and_json(self, db: Database):
        with db.session() as sess:
            from datetime import timezone
            event = sess.get(Event, 1)
            assert event is not None
            assert event.event_action == "create"
            assert event.start_date is not None
            assert event.start_date.tzinfo == timezone.utc
            assert event.property_bag == {"extra": "data"}

    def test_event_source_relationship(self, db: Database):
        with db.session() as sess:
            event = sess.get(Event, 1)
            assert event is not None
            assert event.event_source is not None
            assert event.event_source.title == "Favorite Source"


class TestEventSourceTaskActivity:
    def test_deleted_scope(self, db: Database):
        with db.session() as sess:
            deleted = sess.scalars(EventSourceTaskActivity.deleted()).all()
            assert len(deleted) == 1
            assert deleted[0].id == 2

    def test_non_deleted(self, db: Database):
        with db.session() as sess:
            esta = sess.get(EventSourceTaskActivity, 1)
            assert esta is not None
            assert esta.deleted_at is None


class TestIntegrationProject:
    def test_query(self, db: Database):
        with db.session() as sess:
            ips = sess.scalars(select(IntegrationProject)).all()
            assert len(ips) == 1
            assert ips[0].origin_id == "PROJ"

    def test_relationships(self, db: Database):
        with db.session() as sess:
            ip = sess.get(IntegrationProject, 1)
            assert ip is not None
            assert ip.integration is not None
            assert ip.integration.title == "Jira"
            assert ip.project is not None
            assert ip.project.title == "Root Project"
