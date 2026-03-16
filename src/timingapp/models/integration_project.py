from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase
from timingapp._types import JSONText, UnixTimestamp

if TYPE_CHECKING:
    from timingapp.models.integration import Integration
    from timingapp.models.project import Project


class IntegrationProject(TimingBase):
    __tablename__ = "IntegrationProject"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    integration_id: Mapped[int] = mapped_column("integration_id", Integer)
    title: Mapped[str] = mapped_column("title", String)
    origin_id: Mapped[str | None] = mapped_column("origin_id", String)
    timing_project_id: Mapped[int | None] = mapped_column("timing_project_id", Integer)
    last_modified_origin: Mapped[datetime | None] = mapped_column("last_modified_origin", UnixTimestamp)
    last_modified_timing: Mapped[datetime | None] = mapped_column("last_modified_timing", UnixTimestamp)
    deleted_by_integration_at: Mapped[datetime | None] = mapped_column("deleted_by_integration_at", UnixTimestamp)
    hidden_at: Mapped[datetime | None] = mapped_column("hidden_at", UnixTimestamp)
    property_bag: Mapped[Any | None] = mapped_column("property_bag", JSONText)

    integration: Mapped["Integration | None"] = relationship(
        "Integration",
        foreign_keys="[IntegrationProject.integration_id]",
        primaryjoin="IntegrationProject.integration_id == Integration.id",
    )
    project: Mapped["Project | None"] = relationship(
        "Project",
        foreign_keys="[IntegrationProject.timing_project_id]",
        primaryjoin="IntegrationProject.timing_project_id == Project.id",
    )
