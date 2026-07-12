"""Energy reading model mapped to the energy_readings table."""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.device import Device


class EnergyReading(Base):
    """Time-series consumption reading from an energy device."""

    __tablename__ = "energy_readings"
    __table_args__ = (
        CheckConstraint("power_kw >= 0", name="energy_readings_power_kw_check"),
        CheckConstraint("energy_kwh >= 0", name="energy_readings_energy_kwh_check"),
        UniqueConstraint("device_id", "reading_time"),
        Index("idx_energy_readings_time", "reading_time"),
        Index("idx_energy_readings_device_time", "device_id", "reading_time"),
    )

    reading_id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.device_id", ondelete="CASCADE"),
        nullable=False,
    )
    reading_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    power_kw: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    energy_kwh: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    device: Mapped["Device"] = relationship(back_populates="energy_readings")
