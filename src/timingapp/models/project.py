from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, Integer, LargeBinary, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase
from timingapp._types import JSONText

if TYPE_CHECKING:
    from sqlalchemy.sql import Select


class Project(TimingBase):
    __tablename__ = "Project"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    title: Mapped[str] = mapped_column("title", String)
    parentID: Mapped[int | None] = mapped_column("parentID", Integer)
    listPosition: Mapped[int] = mapped_column("listPosition", Integer)
    isSample: Mapped[bool] = mapped_column("isSample", Boolean, default=False)
    color: Mapped[str] = mapped_column("color", String)
    productivityScore: Mapped[float] = mapped_column("productivityScore", Integer, default=0)
    predicate: Mapped[bytes | None] = mapped_column("predicate", LargeBinary)
    ruleListPosition: Mapped[int] = mapped_column("ruleListPosition", Integer)
    isArchived: Mapped[bool] = mapped_column("isArchived", Boolean, default=False)
    membershipID: Mapped[int | None] = mapped_column("membershipID", Integer)
    property_bag: Mapped[Any | None] = mapped_column("property_bag", JSONText)

    parent: Mapped["Project | None"] = relationship(
        "Project",
        remote_side="Project.id",
        foreign_keys="[Project.parentID]",
        primaryjoin="Project.parentID == Project.id",
        back_populates="children",
    )
    children: Mapped[list["Project"]] = relationship(
        "Project",
        foreign_keys="[Project.parentID]",
        primaryjoin="Project.parentID == Project.id",
        back_populates="parent",
    )

    @classmethod
    def archived(cls) -> "Select[tuple[Project]]":
        return select(cls).where(cls.isArchived == True)  # noqa: E712
