"""Pydantic schemas for users."""

from datetime import datetime

from pydantic import EmailStr, Field

from app.schemas.base import OrmBaseModel


class UserBase(OrmBaseModel):
    """Fields shared by user request and response schemas."""

    full_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., max_length=100)


class UserCreate(UserBase):
    """Request schema for creating a user."""

    password: str = Field(..., min_length=8, max_length=128)


class UserRead(UserBase):
    """Response schema for returning a user."""

    user_id: int
    created_at: datetime | None = None
