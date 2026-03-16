from datetime import timezone

from timingapp._database import Database
from timingapp.models.app_activity import AppActivity
from timingapp.models.app_activity_with_strings import AppActivityWithStrings
from sqlalchemy import select


class TestAppActivity:
    def test_query_all(self, db: Database):
        with db.session() as sess:
            activities = sess.scalars(select(AppActivity)).all()
            assert len(activities) == 2

    def test_deleted_scope(self, db: Database):
        with db.session() as sess:
            deleted = sess.scalars(AppActivity.deleted()).all()
            assert len(deleted) == 1
            assert deleted[0].id == 2

    def test_timestamps_are_utc(self, db: Database):
        with db.session() as sess:
            activity = sess.get(AppActivity, 1)
            assert activity is not None
            assert activity.startDate is not None
            assert activity.startDate.tzinfo == timezone.utc
            assert activity.endDate is not None
            assert activity.endDate.tzinfo == timezone.utc

    def test_device_relationship(self, db: Database):
        with db.session() as sess:
            activity = sess.get(AppActivity, 1)
            assert activity is not None
            assert activity.device is not None
            assert activity.device.name == "MacBook Pro"

    def test_application_relationship(self, db: Database):
        with db.session() as sess:
            activity = sess.get(AppActivity, 1)
            assert activity is not None
            assert activity.application is not None
            assert activity.application.bundleIdentifier == "com.apple.Safari"

    def test_project_relationship(self, db: Database):
        with db.session() as sess:
            activity = sess.get(AppActivity, 1)
            assert activity is not None
            assert activity.project is not None
            assert activity.project.title == "Root Project"

    def test_non_deleted_has_no_deleted_at(self, db: Database):
        with db.session() as sess:
            activity = sess.get(AppActivity, 1)
            assert activity is not None
            assert activity.deleted_at is None


class TestAppActivityWithStrings:
    def test_query(self, db: Database):
        with db.session() as sess:
            activities = sess.scalars(select(AppActivityWithStrings)).all()
            assert len(activities) >= 1

    def test_title_string(self, db: Database):
        with db.session() as sess:
            activity = sess.get(AppActivityWithStrings, 1)
            assert activity is not None
            assert activity.title_string == "Google - Safari"
