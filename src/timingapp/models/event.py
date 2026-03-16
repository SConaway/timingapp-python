from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase
from timingapp._types import JSONText, UnixTimestamp

if TYPE_CHECKING:
    from timingapp.models.event_source import EventSource


class Event(TimingBase):
    __tablename__ = "Event"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    startDate: Mapped[datetime | None] = mapped_column("startDate", UnixTimestamp)
    endDate: Mapped[datetime | None] = mapped_column("endDate", UnixTimestamp)
    title: Mapped[str | None] = mapped_column("title", String)
    notes: Mapped[str | None] = mapped_column("notes", String)
    sourceID: Mapped[int | None] = mapped_column("sourceID", Integer)
    property_bag: Mapped[Any | None] = mapped_column("property_bag", JSONText)

    source: Mapped["EventSource | None"] = relationship(
        "EventSource", foreign_keys=[sourceID], primaryjoin="Event.sourceID == EventSource.id"
    )
