"""Shared Pydantic schema configuration."""

from pydantic import BaseModel, ConfigDict


class OrmBaseModel(BaseModel):
    """Base schema that can read data from SQLAlchemy ORM objects."""

    model_config = ConfigDict(from_attributes=True)
