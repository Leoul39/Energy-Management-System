"""API router for energy forecast resources."""

from app.crud import CRUDRepository
from app.models import EnergyForecast
from app.routers.crud import create_crud_router
from app.schemas import EnergyForecastCreate, EnergyForecastRead, EnergyForecastUpdate


router = create_crud_router(
    repository=CRUDRepository(EnergyForecast, "forecast_id"),
    create_schema=EnergyForecastCreate,
    read_schema=EnergyForecastRead,
    update_schema=EnergyForecastUpdate,
    resource_name="Energy forecast",
    id_path_name="forecast_id",
)
