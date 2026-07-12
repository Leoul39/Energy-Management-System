"""Site model mapped to the sites table."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.alert import Alert
    from app.models.device import Device
    from app.models.energy_forecast import EnergyForecast
    from app.models.user import User


class Site(Base):
    """Physical location where energy devices are monitored."""

    __tablename__ = "sites"

    site_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    site_name: Mapped[str] = mapped_column(String(100), nullable=False)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    user: Mapped["User"] = relationship(back_populates="sites")
    devices: Mapped[list["Device"]] = relationship(
        back_populates="site",
        cascade="all, delete-orphan",
    )
    forecasts: Mapped[list["EnergyForecast"]] = relationship(
        back_populates="site",
        cascade="all, delete-orphan",
    )
    alerts: Mapped[list["Alert"]] = relationship(
        back_populates="site",
        cascade="all, delete-orphan",
    )
