"""Pydantic schemas for request and response validation."""

from app.schemas.alert import AlertCreate, AlertRead, AlertUpdate
from app.schemas.battery_status import BatteryStatusCreate, BatteryStatusRead, BatteryStatusUpdate
from app.schemas.device import DeviceCreate, DeviceRead, DeviceUpdate
from app.schemas.energy_forecast import EnergyForecastCreate, EnergyForecastRead, EnergyForecastUpdate
from app.schemas.energy_reading import EnergyReadingCreate, EnergyReadingRead, EnergyReadingUpdate
from app.schemas.site import SiteCreate, SiteRead, SiteUpdate
from app.schemas.solar_generation import SolarGenerationCreate, SolarGenerationRead, SolarGenerationUpdate
from app.schemas.user import UserCreate, UserRead, UserUpdate

__all__ = [
    "AlertCreate",
    "AlertRead",
    "AlertUpdate",
    "BatteryStatusCreate",
    "BatteryStatusRead",
    "BatteryStatusUpdate",
    "DeviceCreate",
    "DeviceRead",
    "DeviceUpdate",
    "EnergyForecastCreate",
    "EnergyForecastRead",
    "EnergyForecastUpdate",
    "EnergyReadingCreate",
    "EnergyReadingRead",
    "EnergyReadingUpdate",
    "SiteCreate",
    "SiteRead",
    "SiteUpdate",
    "SolarGenerationCreate",
    "SolarGenerationRead",
    "SolarGenerationUpdate",
    "UserCreate",
    "UserRead",
    "UserUpdate",
]
