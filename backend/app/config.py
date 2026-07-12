"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the EMS backend."""

    app_name: str = "Energy Management System API"
    app_version: str = "0.1.0"
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/ems",
        description="SQLAlchemy-compatible PostgreSQL connection URL.",
    )
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


settings = get_settings()
