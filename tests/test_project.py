from timingapp._database import Database
from timingapp.models.project import Project


class TestProject:
    def test_query_all(self, db: Database):
        with db.session() as sess:
            from sqlalchemy import select
            projects = sess.scalars(select(Project)).all()
            assert len(projects) >= 3

    def test_archived_scope(self, db: Database):
        with db.session() as sess:
            archived = sess.scalars(Project.archived()).all()
            assert len(archived) == 1
            assert archived[0].title == "Archived Project"

    def test_property_bag_json(self, db: Database):
        with db.session() as sess:
            project = sess.get(Project, 1)
            assert project is not None
            assert project.property_bag == {"key": "value"}

    def test_self_referential_parent(self, db: Database):
        with db.session() as sess:
            child = sess.get(Project, 2)
            assert child is not None
            assert child.parent is not None
            assert child.parent.id == 1
            assert child.parent.title == "Root Project"

    def test_children_relationship(self, db: Database):
        with db.session() as sess:
            parent = sess.get(Project, 1)
            assert parent is not None
            assert len(parent.children) == 1
            assert parent.children[0].id == 2
