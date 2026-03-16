from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase
from timingapp._types import UnixTimestamp

if TYPE_CHECKING:
    from sqlalchemy.sql import Select

    from timingapp.models.application import Application
    from timingapp.models.device import Device
    from timingapp.models.path import Path
    from timingapp.models.project import Project
    from timingapp.models.title import Title


class AppActivity(TimingBase):
    __tablename__ = "AppActivity"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    localDeviceID: Mapped[int | None] = mapped_column("localDeviceID", Integer)
    startDate: Mapped[datetime | None] = mapped_column("startDate", UnixTimestamp)
    endDate: Mapped[datetime | None] = mapped_column("endDate", UnixTimestamp)
    applicationID: Mapped[int | None] = mapped_column("applicationID", Integer)
    titleID: Mapped[int | None] = mapped_column("titleID", Integer)
    pathID: Mapped[int | None] = mapped_column("pathID", Integer)
    projectID: Mapped[int | None] = mapped_column("projectID", Integer)
    isDeleted: Mapped[bool] = mapped_column("isDeleted", Boolean, default=False)

    device: Mapped["Device | None"] = relationship(
        "Device",
        foreign_keys="[AppActivity.localDeviceID]",
        primaryjoin="AppActivity.localDeviceID == Device.localID",
    )
    application: Mapped["Application | None"] = relationship(
        "Application",
        foreign_keys="[AppActivity.applicationID]",
        primaryjoin="AppActivity.applicationID == Application.id",
    )
    title: Mapped["Title | None"] = relationship(
        "Title",
        foreign_keys="[AppActivity.titleID]",
        primaryjoin="AppActivity.titleID == Title.id",
    )
    path: Mapped["Path | None"] = relationship(
        "Path",
        foreign_keys="[AppActivity.pathID]",
        primaryjoin="AppActivity.pathID == Path.id",
    )
    project: Mapped["Project | None"] = relationship(
        "Project",
        foreign_keys="[AppActivity.projectID]",
        primaryjoin="AppActivity.projectID == Project.id",
    )

    @classmethod
    def deleted(cls) -> "Select[tuple[AppActivity]]":
        return select(cls).where(cls.isDeleted == True)  # noqa: E712
