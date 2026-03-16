from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase

if TYPE_CHECKING:
    from timingapp.models.integration import Integration
    from timingapp.models.project import Project


class IntegrationProject(TimingBase):
    __tablename__ = "IntegrationProject"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    integrationID: Mapped[int | None] = mapped_column("integrationID", Integer)
    projectID: Mapped[int | None] = mapped_column("projectID", Integer)
    external_id: Mapped[str | None] = mapped_column("external_id", String)

    integration: Mapped["Integration | None"] = relationship(
        "Integration", foreign_keys=[integrationID], primaryjoin="IntegrationProject.integrationID == Integration.id"
    )
    project: Mapped["Project | None"] = relationship(
        "Project", foreign_keys=[projectID], primaryjoin="IntegrationProject.projectID == Project.id"
    )
