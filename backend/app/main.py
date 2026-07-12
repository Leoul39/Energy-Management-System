"""FastAPI application entrypoint for the Energy Management System backend."""

from fastapi import FastAPI

from app.config import settings
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    configure_logging()

    return FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Backend API for an Energy Management System.",
    )


app = create_app()


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return a simple health response for deployment and local checks."""
    return {"status": "ok"}
