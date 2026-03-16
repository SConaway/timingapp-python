from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from timingapp._base import TimingBase


class Integration(TimingBase):
    __tablename__ = "Integration"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    name: Mapped[str | None] = mapped_column("name", String)
    type: Mapped[str | None] = mapped_column("type", String)
    configuration: Mapped[str | None] = mapped_column("configuration", String)
