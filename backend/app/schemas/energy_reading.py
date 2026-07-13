"""Pydantic schemas for energy readings."""

from datetime import datetime
from decimal import Decimal

from pydantic import Field

from app.schemas.base import OrmBaseModel


class EnergyReadingBase(OrmBaseModel):
    """Fields shared by energy reading request and response schemas."""

    reading_time: datetime
    power_kw: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    energy_kwh: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)


class EnergyReadingCreate(EnergyReadingBase):
    """Request schema for creating an energy reading."""

    device_id: int = Field(..., gt=0)


class EnergyReadingRead(EnergyReadingBase):
    """Response schema for returning an energy reading."""

    reading_id: int
    device_id: int
    created_at: datetime | None = None
