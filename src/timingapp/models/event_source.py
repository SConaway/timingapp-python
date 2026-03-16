from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase

if TYPE_CHECKING:
    from sqlalchemy.sql import Select


class EventSource(TimingBase):
    __tablename__ = "EventSource"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    name: Mapped[str | None] = mapped_column("name", String)
    type: Mapped[str | None] = mapped_column("type", String)
    is_template: Mapped[int | None] = mapped_column("is_template", Integer)
    is_favorite: Mapped[int | None] = mapped_column("is_favorite", Integer)
    templateID: Mapped[int | None] = mapped_column("templateID", Integer)

    template: Mapped["EventSource | None"] = relationship(
        "EventSource",
        remote_side="EventSource.id",
        foreign_keys="[EventSource.templateID]",
        primaryjoin="EventSource.templateID == EventSource.id",
        back_populates="instances",
    )
    instances: Mapped[list["EventSource"]] = relationship(
        "EventSource",
        foreign_keys="[EventSource.templateID]",
        primaryjoin="EventSource.templateID == EventSource.id",
        back_populates="template",
    )

    @classmethod
    def templates(cls) -> "Select[tuple[EventSource]]":
        return select(cls).where(cls.is_template == 1)

    @classmethod
    def favorites(cls) -> "Select[tuple[EventSource]]":
        return select(cls).where(cls.is_favorite == 1)
