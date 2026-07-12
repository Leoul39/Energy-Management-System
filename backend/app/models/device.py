"""Device model mapped to the devices table."""

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.battery_status import BatteryStatus
    from app.models.energy_reading import EnergyReading
    from app.models.site import Site
    from app.models.solar_generation import SolarGeneration


class Device(Base):
    """Energy-related device installed at a monitored site."""

    __tablename__ = "devices"

    device_id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(
        ForeignKey("sites.site_id", ondelete="CASCADE"),
        nullable=False,
    )
    device_name: Mapped[str] = mapped_column(String(100), nullable=False)
    device_type: Mapped[str] = mapped_column(String(50), nullable=False)
    manufacturer: Mapped[str | None] = mapped_column(String(100))
    installed_at: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    site: Mapped["Site"] = relationship(back_populates="devices")
    energy_readings: Mapped[list["EnergyReading"]] = relationship(
        back_populates="device",
        cascade="all, delete-orphan",
    )
    solar_generation_records: Mapped[list["SolarGeneration"]] = relationship(
        back_populates="device",
        cascade="all, delete-orphan",
    )
    battery_status_records: Mapped[list["BatteryStatus"]] = relationship(
        back_populates="device",
        cascade="all, delete-orphan",
    )
