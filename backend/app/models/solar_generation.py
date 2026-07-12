"""Solar generation model mapped to the solar_generation table."""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.device import Device


class SolarGeneration(Base):
    """Time-series solar production reading from a solar device."""

    __tablename__ = "solar_generation"
    __table_args__ = (
        CheckConstraint("generated_kwh >= 0", name="solar_generation_generated_kwh_check"),
        Index("idx_solar_generation_time", "generated_at"),
    )

    generation_id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.device_id", ondelete="CASCADE"),
        nullable=False,
    )
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    generated_kwh: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    device: Mapped["Device"] = relationship(back_populates="solar_generation_records")
