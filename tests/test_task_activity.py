from datetime import timezone

from sqlalchemy import select

from timingapp._database import Database
from timingapp.models.task_activity import TaskActivity


class TestTaskActivity:
    def test_query_all(self, db: Database):
        with db.session() as sess:
            activities = sess.scalars(select(TaskActivity)).all()
            assert len(activities) == 3

    def test_running_scope(self, db: Database):
        with db.session() as sess:
            running = sess.scalars(TaskActivity.running()).all()
            assert len(running) == 1
            assert running[0].id == 1

    def test_deleted_scope(self, db: Database):
        with db.session() as sess:
            deleted = sess.scalars(TaskActivity.deleted()).all()
            assert len(deleted) == 1
            assert deleted[0].id == 3

    def test_property_bag_json(self, db: Database):
        with db.session() as sess:
            activity = sess.get(TaskActivity, 1)
            assert activity is not None
            assert activity.property_bag == {"tag": "dev"}

    def test_title_and_notes(self, db: Database):
        with db.session() as sess:
            activity = sess.get(TaskActivity, 1)
            assert activity is not None
            assert activity.title == "Feature work"
            assert activity.notes == "Working on feature"

    def test_timestamps_are_utc(self, db: Database):
        with db.session() as sess:
            activity = sess.get(TaskActivity, 2)
            assert activity is not None
            assert activity.startDate is not None
            assert activity.startDate.tzinfo == timezone.utc

    def test_project_relationship(self, db: Database):
        with db.session() as sess:
            activity = sess.get(TaskActivity, 1)
            assert activity is not None
            assert activity.project is not None
            assert activity.project.title == "Root Project"
