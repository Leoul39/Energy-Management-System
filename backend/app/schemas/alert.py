"""Pydantic schemas for alerts."""

from datetime import datetime

from pydantic import Field

from app.schemas.base import OrmBaseModel


class AlertBase(OrmBaseModel):
    """Fields shared by alert request and response schemas."""

    alert_type: str = Field(..., min_length=1, max_length=50)
    message: str = Field(..., min_length=1)
    status: str = Field(default="unread", min_length=1, max_length=20)
    acknowledged_at: datetime | None = None


class AlertCreate(AlertBase):
    """Request schema for creating an alert."""

    site_id: int = Field(..., gt=0)


class AlertUpdate(OrmBaseModel):
    """Request schema for partially updating an alert."""

    status: str | None = Field(default=None, min_length=1, max_length=20)
    acknowledged_at: datetime | None = None


class AlertRead(AlertBase):
    """Response schema for returning an alert."""

    alert_id: int
    site_id: int
    created_at: datetime | None = None
