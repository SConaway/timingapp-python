from datetime import datetime

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from timingapp._base import TimingBase
from timingapp._types import UnixTimestamp


class AppActivityWithStrings(TimingBase):
    __tablename__ = "AppActivityWithStrings"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    localDeviceID: Mapped[int | None] = mapped_column("localDeviceID", Integer)
    startDate: Mapped[datetime | None] = mapped_column("startDate", UnixTimestamp)
    endDate: Mapped[datetime | None] = mapped_column("endDate", UnixTimestamp)
    applicationID: Mapped[int | None] = mapped_column("applicationID", Integer)
    titleID: Mapped[int | None] = mapped_column("titleID", Integer)
    pathID: Mapped[int | None] = mapped_column("pathID", Integer)
    # The view selects Title.stringValue then Path.stringValue; SQLite names
    # the duplicate "stringValue:1" in the virtual column list.
    title_string: Mapped[str | None] = mapped_column("stringValue", String, key="title_string")
    path_string: Mapped[str | None] = mapped_column("stringValue:1", String, key="path_string")
    projectID: Mapped[int | None] = mapped_column("projectID", Integer)
