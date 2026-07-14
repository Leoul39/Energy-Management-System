"""API router for energy reading resources."""

from app.crud import CRUDRepository
from app.models import EnergyReading
from app.routers.crud import create_crud_router
from app.schemas import EnergyReadingCreate, EnergyReadingRead, EnergyReadingUpdate


router = create_crud_router(
    repository=CRUDRepository(EnergyReading, "reading_id"),
    create_schema=EnergyReadingCreate,
    read_schema=EnergyReadingRead,
    update_schema=EnergyReadingUpdate,
    resource_name="Energy reading",
    id_path_name="reading_id",
)
