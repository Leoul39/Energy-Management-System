"""Pydantic schemas for devices."""

from datetime import date, datetime

from pydantic import Field

from app.schemas.base import OrmBaseModel


class DeviceBase(OrmBaseModel):
    """Fields shared by device request and response schemas."""

    device_name: str = Field(..., min_length=1, max_length=100)
    device_type: str = Field(..., min_length=1, max_length=50)
    manufacturer: str | None = Field(default=None, max_length=100)
    installed_at: date | None = None


class DeviceCreate(DeviceBase):
    """Request schema for creating a device."""

    site_id: int = Field(..., gt=0)


class DeviceUpdate(OrmBaseModel):
    """Request schema for partially updating a device."""

    device_name: str | None = Field(default=None, min_length=1, max_length=100)
    device_type: str | None = Field(default=None, min_length=1, max_length=50)
    manufacturer: str | None = Field(default=None, max_length=100)
    installed_at: date | None = None


class DeviceRead(DeviceBase):
    """Response schema for returning a device."""

    device_id: int
    site_id: int
    created_at: datetime | None = None
