from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import Integer, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase
from timingapp._types import JSONText, UnixTimestamp

if TYPE_CHECKING:
    from sqlalchemy.sql import Select

    from timingapp.models.event import Event
    from timingapp.models.event_source import EventSource
    from timingapp.models.task_activity import TaskActivity


class EventSourceTaskActivity(TimingBase):
    __tablename__ = "EventSourceTaskActivity"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    integration_id: Mapped[int] = mapped_column("integration_id", Integer)
    event_source_id: Mapped[int] = mapped_column("event_source_id", Integer)
    task_activity_id: Mapped[int] = mapped_column("task_activity_id", Integer)
    deleted_at: Mapped[datetime | None] = mapped_column("deleted_at", UnixTimestamp)
    property_bag: Mapped[Any | None] = mapped_column("property_bag", JSONText)
    event_id: Mapped[int | None] = mapped_column("event_id", Integer)

    event_source: Mapped["EventSource | None"] = relationship(
        "EventSource",
        foreign_keys="[EventSourceTaskActivity.event_source_id]",
        primaryjoin="EventSourceTaskActivity.event_source_id == EventSource.id",
    )
    task_activity: Mapped["TaskActivity | None"] = relationship(
        "TaskActivity",
        foreign_keys="[EventSourceTaskActivity.task_activity_id]",
        primaryjoin="EventSourceTaskActivity.task_activity_id == TaskActivity.id",
    )
    event: Mapped["Event | None"] = relationship(
        "Event",
        foreign_keys="[EventSourceTaskActivity.event_id]",
        primaryjoin="EventSourceTaskActivity.event_id == Event.id",
    )

    @classmethod
    def deleted(cls) -> "Select[tuple[EventSourceTaskActivity]]":
        return select(cls).where(cls.deleted_at.is_not(None))
