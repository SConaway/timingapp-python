from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from timingapp._base import TimingBase


class Device(TimingBase):
    __tablename__ = "Device"

    localID: Mapped[int] = mapped_column("localID", Integer, primary_key=True)
    name: Mapped[str | None] = mapped_column("name", String)
    uuid: Mapped[str | None] = mapped_column("uuid", String)
    local_device: Mapped[int | None] = mapped_column("local_device", Integer)
