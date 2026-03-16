from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase
from timingapp._types import JSONText, UnixTimestamp

if TYPE_CHECKING:
    from sqlalchemy.sql import Select

    from timingapp.models.integration import Integration
    from timingapp.models.integration_project import IntegrationProject


class EventSource(TimingBase):
    __tablename__ = "EventSource"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    integration_id: Mapped[int] = mapped_column("integration_id", Integer)
    integration_project_id: Mapped[int | None] = mapped_column("integration_project_id", Integer)
    template_id: Mapped[int | None] = mapped_column("template_id", Integer)
    is_template: Mapped[bool] = mapped_column("is_template", Boolean, default=False)
    title: Mapped[str] = mapped_column("title", String)
    notes: Mapped[str | None] = mapped_column("notes", String)
    event_source_type: Mapped[str] = mapped_column("event_source_type", String)
    origin_id: Mapped[str | None] = mapped_column("origin_id", String)
    is_favorite: Mapped[bool] = mapped_column("is_favorite", Boolean, default=False)
    last_modified_origin: Mapped[datetime | None] = mapped_column("last_modified_origin", UnixTimestamp)
    last_modified_timing: Mapped[datetime | None] = mapped_column("last_modified_timing", UnixTimestamp)
    created_by_integration_at: Mapped[datetime | None] = mapped_column("created_by_integration_at", UnixTimestamp)
    deleted_by_integration_at: Mapped[datetime | None] = mapped_column("deleted_by_integration_at", UnixTimestamp)
    hidden_at: Mapped[datetime | None] = mapped_column("hidden_at", UnixTimestamp)
    property_bag: Mapped[Any | None] = mapped_column("property_bag", JSONText)

    integration: Mapped["Integration | None"] = relationship(
        "Integration",
        foreign_keys="[EventSource.integration_id]",
        primaryjoin="EventSource.integration_id == Integration.id",
    )
    integration_project: Mapped["IntegrationProject | None"] = relationship(
        "IntegrationProject",
        foreign_keys="[EventSource.integration_project_id]",
        primaryjoin="EventSource.integration_project_id == IntegrationProject.id",
    )
    template: Mapped["EventSource | None"] = relationship(
        "EventSource",
        remote_side="EventSource.id",
        foreign_keys="[EventSource.template_id]",
        primaryjoin="EventSource.template_id == EventSource.id",
        back_populates="instances",
    )
    instances: Mapped[list["EventSource"]] = relationship(
        "EventSource",
        foreign_keys="[EventSource.template_id]",
        primaryjoin="EventSource.template_id == EventSource.id",
        back_populates="template",
    )

    @classmethod
    def templates(cls) -> "Select[tuple[EventSource]]":
        return select(cls).where(cls.is_template == True)  # noqa: E712

    @classmethod
    def favorites(cls) -> "Select[tuple[EventSource]]":
        return select(cls).where(cls.is_favorite == True)  # noqa: E712
