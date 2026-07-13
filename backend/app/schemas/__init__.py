"""Pydantic schemas for request and response validation."""

from app.schemas.alert import AlertCreate, AlertRead, AlertUpdate
from app.schemas.battery_status import BatteryStatusCreate, BatteryStatusRead
from app.schemas.device import DeviceCreate, DeviceRead, DeviceUpdate
from app.schemas.energy_forecast import EnergyForecastCreate, EnergyForecastRead
from app.schemas.energy_reading import EnergyReadingCreate, EnergyReadingRead
from app.schemas.site import SiteCreate, SiteRead, SiteUpdate
from app.schemas.solar_generation import SolarGenerationCreate, SolarGenerationRead
from app.schemas.user import UserCreate, UserRead

__all__ = [
    "AlertCreate",
    "AlertRead",
    "AlertUpdate",
    "BatteryStatusCreate",
    "BatteryStatusRead",
    "DeviceCreate",
    "DeviceRead",
    "DeviceUpdate",
    "EnergyForecastCreate",
    "EnergyForecastRead",
    "EnergyReadingCreate",
    "EnergyReadingRead",
    "SiteCreate",
    "SiteRead",
    "SiteUpdate",
    "SolarGenerationCreate",
    "SolarGenerationRead",
    "UserCreate",
    "UserRead",
]
