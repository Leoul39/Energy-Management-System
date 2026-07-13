"""Pydantic schemas for sites."""

from datetime import datetime

from pydantic import Field

from app.schemas.base import OrmBaseModel


class SiteBase(OrmBaseModel):
    """Fields shared by site request and response schemas."""

    site_name: str = Field(..., min_length=1, max_length=100)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class SiteCreate(SiteBase):
    """Request schema for creating a site."""

    user_id: int = Field(..., gt=0)


class SiteUpdate(OrmBaseModel):
    """Request schema for partially updating a site."""

    site_name: str | None = Field(default=None, min_length=1, max_length=100)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class SiteRead(SiteBase):
    """Response schema for returning a site."""

    site_id: int
    user_id: int
    created_at: datetime | None = None
