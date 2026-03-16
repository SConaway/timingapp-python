from typing import Any

from sqlalchemy import Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from timingapp._base import TimingBase
from timingapp._types import JSONText


class Device(TimingBase):
    __tablename__ = "Device"

    localID: Mapped[int] = mapped_column("localID", Integer, primary_key=True)
    globalID: Mapped[int] = mapped_column("globalID", Integer)
    macAddress: Mapped[bytes | None] = mapped_column("macAddress", LargeBinary)
    displayName: Mapped[str | None] = mapped_column("displayName", String)
    property_bag: Mapped[Any | None] = mapped_column("property_bag", JSONText)
