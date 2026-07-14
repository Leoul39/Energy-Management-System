"""API route modules for the FastAPI application."""

from app.routers import (
    alerts,
    battery_status,
    devices,
    energy_forecasts,
    energy_readings,
    sites,
    solar_generation,
    users,
)

__all__ = [
    "alerts",
    "battery_status",
    "devices",
    "energy_forecasts",
    "energy_readings",
    "sites",
    "solar_generation",
    "users",
]
