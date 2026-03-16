from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase
from timingapp._types import JSONText, UnixTimestamp

if TYPE_CHECKING:
    from timingapp.models.event_source import EventSource
    from timingapp.models.integration import Integration


class Event(TimingBase):
    __tablename__ = "Event"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    integration_id: Mapped[int] = mapped_column("integration_id", Integer)
    event_source_id: Mapped[int] = mapped_column("event_source_id", Integer)
    start_date: Mapped[datetime | None] = mapped_column("start_date", UnixTimestamp)
    end_date: Mapped[datetime | None] = mapped_column("end_date", UnixTimestamp)
    origin_id: Mapped[str | None] = mapped_column("origin_id", String)
    event_action: Mapped[str] = mapped_column("event_action", String)
    last_modified_origin: Mapped[datetime | None] = mapped_column("last_modified_origin", UnixTimestamp)
    last_modified_timing: Mapped[datetime | None] = mapped_column("last_modified_timing", UnixTimestamp)
    deleted_at: Mapped[datetime | None] = mapped_column("deleted_at", UnixTimestamp)
    property_bag: Mapped[Any | None] = mapped_column("property_bag", JSONText)

    integration: Mapped["Integration | None"] = relationship(
        "Integration",
        foreign_keys="[Event.integration_id]",
        primaryjoin="Event.integration_id == Integration.id",
    )
    event_source: Mapped["EventSource | None"] = relationship(
        "EventSource",
        foreign_keys="[Event.event_source_id]",
        primaryjoin="Event.event_source_id == EventSource.id",
    )
