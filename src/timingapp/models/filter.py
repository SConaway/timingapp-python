from typing import TYPE_CHECKING, Any

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase
from timingapp._types import JSONText

if TYPE_CHECKING:
    from sqlalchemy.sql import Select


class Filter(TimingBase):
    __tablename__ = "Filter"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    name: Mapped[str | None] = mapped_column("name", String)
    parentID: Mapped[int | None] = mapped_column("parentID", Integer)
    is_sample: Mapped[int | None] = mapped_column("is_sample", Integer)
    criteria: Mapped[Any | None] = mapped_column("criteria", JSONText)

    parent: Mapped["Filter | None"] = relationship(
        "Filter",
        remote_side="Filter.id",
        foreign_keys="[Filter.parentID]",
        primaryjoin="Filter.parentID == Filter.id",
        back_populates="children",
    )
    children: Mapped[list["Filter"]] = relationship(
        "Filter",
        foreign_keys="[Filter.parentID]",
        primaryjoin="Filter.parentID == Filter.id",
        back_populates="parent",
    )

    @classmethod
    def samples(cls) -> "Select[tuple[Filter]]":
        return select(cls).where(cls.is_sample == 1)
