from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase
from timingapp._types import JSONText, UnixTimestamp

if TYPE_CHECKING:
    from sqlalchemy.sql import Select

    from timingapp.models.project import Project


class TaskActivity(TimingBase):
    __tablename__ = "TaskActivity"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    startDate: Mapped[datetime | None] = mapped_column("startDate", UnixTimestamp)
    endDate: Mapped[datetime | None] = mapped_column("endDate", UnixTimestamp)
    projectID: Mapped[int | None] = mapped_column("projectID", Integer)
    title: Mapped[str | None] = mapped_column("title", String)
    notes: Mapped[str | None] = mapped_column("notes", String)
    isDeleted: Mapped[bool] = mapped_column("isDeleted", Boolean, default=False)
    isRunning: Mapped[bool] = mapped_column("isRunning", Boolean, default=False)
    property_bag: Mapped[Any | None] = mapped_column("property_bag", JSONText)

    project: Mapped["Project | None"] = relationship(
        "Project",
        foreign_keys="[TaskActivity.projectID]",
        primaryjoin="TaskActivity.projectID == Project.id",
    )

    @classmethod
    def running(cls) -> "Select[tuple[TaskActivity]]":
        return select(cls).where(cls.isRunning == True)  # noqa: E712

    @classmethod
    def deleted(cls) -> "Select[tuple[TaskActivity]]":
        return select(cls).where(cls.isDeleted == True)  # noqa: E712
