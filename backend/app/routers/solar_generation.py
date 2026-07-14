"""API router for solar generation resources."""

from app.crud import CRUDRepository
from app.models import SolarGeneration
from app.routers.crud import create_crud_router
from app.schemas import SolarGenerationCreate, SolarGenerationRead, SolarGenerationUpdate


router = create_crud_router(
    repository=CRUDRepository(SolarGeneration, "generation_id"),
    create_schema=SolarGenerationCreate,
    read_schema=SolarGenerationRead,
    update_schema=SolarGenerationUpdate,
    resource_name="Solar generation record",
    id_path_name="generation_id",
)
