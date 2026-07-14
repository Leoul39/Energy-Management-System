"""Pydantic schemas for solar generation records."""

from datetime import datetime
from decimal import Decimal

from pydantic import Field

from app.schemas.base import OrmBaseModel


class SolarGenerationBase(OrmBaseModel):
    """Fields shared by solar generation request and response schemas."""

    generated_at: datetime
    generated_kwh: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2)


class SolarGenerationCreate(SolarGenerationBase):
    """Request schema for creating a solar generation record."""

    device_id: int = Field(..., gt=0)


class SolarGenerationUpdate(OrmBaseModel):
    """Request schema for partially updating a solar generation record."""

    generated_at: datetime | None = None
    generated_kwh: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)


class SolarGenerationRead(SolarGenerationBase):
    """Response schema for returning a solar generation record."""

    generation_id: int
    device_id: int
    created_at: datetime | None = None
