from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from timingapp._base import TimingBase


class Path(TimingBase):
    __tablename__ = "Path"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    stringValue: Mapped[str | None] = mapped_column("stringValue", String)
