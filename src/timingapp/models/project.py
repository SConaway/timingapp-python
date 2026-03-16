from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase
from timingapp._types import JSONText

if TYPE_CHECKING:
    from sqlalchemy.sql import Select


class Project(TimingBase):
    __tablename__ = "Project"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    title: Mapped[str | None] = mapped_column("title", String)
    color: Mapped[str | None] = mapped_column("color", String)
    parentID: Mapped[int | None] = mapped_column("parentID", Integer)
    is_archived: Mapped[int | None] = mapped_column("is_archived", Integer)
    property_bag: Mapped[dict | None] = mapped_column("property_bag", JSONText)

    parent: Mapped["Project | None"] = relationship(
        "Project",
        remote_side="Project.id",
        foreign_keys="[Project.parentID]",
        primaryjoin="Project.parentID == Project.id",
        back_populates="children",
    )
    children: Mapped[list["Project"]] = relationship(
        "Project",
        foreign_keys="[Project.parentID]",
        primaryjoin="Project.parentID == Project.id",
        back_populates="parent",
    )

    @classmethod
    def archived(cls) -> "Select[tuple[Project]]":
        return select(cls).where(cls.is_archived == 1)
