"""Pydantic schemas for battery status records."""

from datetime import datetime
from decimal import Decimal

from pydantic import Field

from app.schemas.base import OrmBaseModel


class BatteryStatusBase(OrmBaseModel):
    """Fields shared by battery status request and response schemas."""

    recorded_at: datetime
    charge_percent: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
        max_digits=5,
        decimal_places=2,
    )
    charge_kwh: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)


class BatteryStatusCreate(BatteryStatusBase):
    """Request schema for creating a battery status record."""

    device_id: int = Field(..., gt=0)


class BatteryStatusUpdate(OrmBaseModel):
    """Request schema for partially updating a battery status record."""

    recorded_at: datetime | None = None
    charge_percent: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
        max_digits=5,
        decimal_places=2,
    )
    charge_kwh: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)


class BatteryStatusRead(BatteryStatusBase):
    """Response schema for returning a battery status record."""

    battery_status_id: int
    device_id: int
    created_at: datetime | None = None
