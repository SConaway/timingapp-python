from datetime import datetime

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from timingapp._base import TimingBase
from timingapp._types import UnixTimestamp


class AppActivityWithStrings(TimingBase):
    __tablename__ = "AppActivityWithStrings"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    startDate: Mapped[datetime | None] = mapped_column("startDate", UnixTimestamp)
    endDate: Mapped[datetime | None] = mapped_column("endDate", UnixTimestamp)
    bundleIdentifier: Mapped[str | None] = mapped_column("bundleIdentifier", String)
    app_name: Mapped[str | None] = mapped_column("app_name", String)
    title_string: Mapped[str | None] = mapped_column("stringValue", String, key="title_string")
    projectID: Mapped[int | None] = mapped_column("projectID", Integer)
    project_title: Mapped[str | None] = mapped_column("project_title", String)
    deviceID: Mapped[int | None] = mapped_column("deviceID", Integer)
