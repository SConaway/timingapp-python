from datetime import datetime
from typing import Any

from sqlalchemy import Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from timingapp._base import TimingBase
from timingapp._types import JSONText, UnixTimestamp


class Integration(TimingBase):
    __tablename__ = "Integration"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    origin_id: Mapped[str] = mapped_column("origin_id", String)
    type: Mapped[str] = mapped_column("type", String)
    title: Mapped[str] = mapped_column("title", String)
    icon: Mapped[bytes | None] = mapped_column("icon", LargeBinary)
    enabled_at: Mapped[datetime | None] = mapped_column("enabled_at", UnixTimestamp)
    last_updated_at: Mapped[datetime | None] = mapped_column("last_updated_at", UnixTimestamp)
    paused_at: Mapped[datetime | None] = mapped_column("paused_at", UnixTimestamp)
    deleted_at: Mapped[datetime | None] = mapped_column("deleted_at", UnixTimestamp)
    last_modified_origin: Mapped[datetime | None] = mapped_column("last_modified_origin", UnixTimestamp)
    last_modified_timing: Mapped[datetime | None] = mapped_column("last_modified_timing", UnixTimestamp)
    version: Mapped[int] = mapped_column("version", Integer)
    api_status: Mapped[str | None] = mapped_column("api_status", String)
    event_visibility: Mapped[str] = mapped_column("event_visibility", String)
    property_bag: Mapped[Any | None] = mapped_column("property_bag", JSONText)
