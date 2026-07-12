"""Energy forecast model mapped to the energy_forecasts table."""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.site import Site


class EnergyForecast(Base):
    """Machine-learning forecast record for a monitored site."""

    __tablename__ = "energy_forecasts"
    __table_args__ = (
        CheckConstraint("predicted_kwh >= 0", name="energy_forecasts_predicted_kwh_check"),
        Index("idx_energy_forecasts_time", "forecast_time"),
    )

    forecast_id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(
        ForeignKey("sites.site_id", ondelete="CASCADE"),
        nullable=False,
    )
    forecast_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    predicted_kwh: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    model_name: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    site: Mapped["Site"] = relationship(back_populates="forecasts")
