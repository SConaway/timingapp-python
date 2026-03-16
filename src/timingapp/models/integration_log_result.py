from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase
from timingapp._types import UnixTimestamp

if TYPE_CHECKING:
    from timingapp.models.integration import Integration


class IntegrationLogResult(TimingBase):
    __tablename__ = "integration_log_result"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    integration_id: Mapped[int] = mapped_column("integration_id", Integer)
    result: Mapped[int] = mapped_column("result", Integer)
    error_message: Mapped[str | None] = mapped_column("error_message", String)
    timestamp: Mapped[datetime | None] = mapped_column("timestamp", UnixTimestamp)

    integration: Mapped["Integration | None"] = relationship(
        "Integration",
        foreign_keys="[IntegrationLogResult.integration_id]",
        primaryjoin="IntegrationLogResult.integration_id == Integration.id",
    )
