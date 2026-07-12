"""Battery status model mapped to the battery_status table."""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.device import Device


class BatteryStatus(Base):
    """Time-series battery state reading from a battery device."""

    __tablename__ = "battery_status"
    __table_args__ = (
        CheckConstraint(
            "charge_percent >= 0 AND charge_percent <= 100",
            name="battery_status_charge_percent_check",
        ),
        CheckConstraint("charge_kwh >= 0", name="battery_status_charge_kwh_check"),
        Index("idx_battery_status_time", "recorded_at"),
    )

    battery_status_id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.device_id", ondelete="CASCADE"),
        nullable=False,
    )
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    charge_percent: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    charge_kwh: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    device: Mapped["Device"] = relationship(back_populates="battery_status_records")
