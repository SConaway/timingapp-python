from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from timingapp._base import TimingBase
from timingapp._types import JSONText
from typing import Any


class Application(TimingBase):
    __tablename__ = "Application"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    bundleIdentifier: Mapped[str | None] = mapped_column("bundleIdentifier", String)
    executable: Mapped[str | None] = mapped_column("executable", String)
    title: Mapped[str | None] = mapped_column("title", String)
    property_bag: Mapped[Any | None] = mapped_column("property_bag", JSONText)
