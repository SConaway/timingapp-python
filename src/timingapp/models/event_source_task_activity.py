from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase
from timingapp._types import UnixTimestamp

if TYPE_CHECKING:
    from sqlalchemy.sql import Select

    from timingapp.models.event_source import EventSource
    from timingapp.models.task_activity import TaskActivity


class EventSourceTaskActivity(TimingBase):
    __tablename__ = "EventSourceTaskActivity"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    eventSourceID: Mapped[int | None] = mapped_column("eventSourceID", Integer)
    taskActivityID: Mapped[int | None] = mapped_column("taskActivityID", Integer)
    deleted_at: Mapped[datetime | None] = mapped_column("deleted_at", UnixTimestamp)

    event_source: Mapped["EventSource | None"] = relationship(
        "EventSource", foreign_keys=[eventSourceID], primaryjoin="EventSourceTaskActivity.eventSourceID == EventSource.id"
    )
    task_activity: Mapped["TaskActivity | None"] = relationship(
        "TaskActivity", foreign_keys=[taskActivityID], primaryjoin="EventSourceTaskActivity.taskActivityID == TaskActivity.id"
    )

    @classmethod
    def deleted(cls) -> "Select[tuple[EventSourceTaskActivity]]":
        return select(cls).where(cls.deleted_at.is_not(None))
