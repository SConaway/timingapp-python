from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from timingapp._base import TimingBase


class Application(TimingBase):
    __tablename__ = "Application"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    bundleIdentifier: Mapped[str | None] = mapped_column("bundleIdentifier", String)
    name: Mapped[str | None] = mapped_column("name", String)
    category: Mapped[str | None] = mapped_column("category", String)
    is_productivity_app: Mapped[int | None] = mapped_column("is_productivity_app", Integer)
