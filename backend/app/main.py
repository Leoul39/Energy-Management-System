"""FastAPI application entrypoint for the Energy Management System backend."""

from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings
from app.core.logging import configure_logging
from app.database import SessionLocal
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


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Backend API for an Energy Management System.",
    )

    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(sites.router, prefix="/sites", tags=["sites"])
    app.include_router(devices.router, prefix="/devices", tags=["devices"])
    app.include_router(energy_readings.router, prefix="/energy-readings", tags=["energy readings"])
    app.include_router(solar_generation.router, prefix="/solar-generation", tags=["solar generation"])
    app.include_router(battery_status.router, prefix="/battery-status", tags=["battery status"])
    app.include_router(energy_forecasts.router, prefix="/forecasts", tags=["forecasts"])
    app.include_router(alerts.router, prefix="/alerts", tags=["alerts"])

    return app


app = create_app()


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return a simple health response for deployment and local checks."""
    return {"status": "ok"}


@app.get("/health/db", tags=["health"])
def database_health_check() -> dict[str, str]:
    """Return database connectivity status."""
    try:
        with SessionLocal() as db_session:
            db_session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return {
            "status": "error",
            "message": "Database connection failed. Check DATABASE_URL in .env.",
        }

    return {"status": "ok"}
