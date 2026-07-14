"""Pydantic schemas for energy forecasts."""

from datetime import datetime
from decimal import Decimal

from pydantic import Field

from app.schemas.base import OrmBaseModel


class EnergyForecastBase(OrmBaseModel):
    """Fields shared by energy forecast request and response schemas."""

    forecast_time: datetime
    predicted_kwh: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2)
    model_name: str | None = Field(default=None, max_length=50)


class EnergyForecastCreate(EnergyForecastBase):
    """Request schema for creating an energy forecast."""

    site_id: int = Field(..., gt=0)


class EnergyForecastUpdate(OrmBaseModel):
    """Request schema for partially updating an energy forecast."""

    forecast_time: datetime | None = None
    predicted_kwh: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    model_name: str | None = Field(default=None, max_length=50)


class EnergyForecastRead(EnergyForecastBase):
    """Response schema for returning an energy forecast."""

    forecast_id: int
    site_id: int
    created_at: datetime | None = None
