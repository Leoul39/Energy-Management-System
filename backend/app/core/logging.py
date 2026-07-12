"""Logging configuration for the backend application."""

import logging

from app.config import settings


def configure_logging() -> None:
    """Configure process-wide logging with the configured log level."""
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
