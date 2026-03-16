from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, Integer, LargeBinary, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase
from timingapp._types import JSONText

if TYPE_CHECKING:
    from sqlalchemy.sql import Select


class Filter(TimingBase):
    __tablename__ = "Filter"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    parentID: Mapped[int | None] = mapped_column("parentID", Integer)
    listPosition: Mapped[int] = mapped_column("listPosition", Integer)
    title: Mapped[str] = mapped_column("title", String)
    predicate: Mapped[bytes | None] = mapped_column("predicate", LargeBinary)
    isSample: Mapped[bool] = mapped_column("isSample", Boolean, default=False)
    property_bag: Mapped[Any | None] = mapped_column("property_bag", JSONText)

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
        return select(cls).where(cls.isSample == True)  # noqa: E712
