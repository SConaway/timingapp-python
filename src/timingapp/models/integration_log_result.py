from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timingapp._base import TimingBase
from timingapp._types import JSONText, UnixTimestamp

if TYPE_CHECKING:
    from timingapp.models.integration import Integration


class IntegrationLogResult(TimingBase):
    __tablename__ = "integration_log_result"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    integrationID: Mapped[int | None] = mapped_column("integrationID", Integer)
    timestamp: Mapped[datetime | None] = mapped_column("timestamp", UnixTimestamp)
    result: Mapped[str | None] = mapped_column("result", String)
    details: Mapped[Any | None] = mapped_column("details", JSONText)

    integration: Mapped["Integration | None"] = relationship(
        "Integration", foreign_keys=[integrationID], primaryjoin="IntegrationLogResult.integrationID == Integration.id"
    )
