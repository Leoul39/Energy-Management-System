"""API router for battery status resources."""

from app.crud import CRUDRepository
from app.models import BatteryStatus
from app.routers.crud import create_crud_router
from app.schemas import BatteryStatusCreate, BatteryStatusRead, BatteryStatusUpdate


router = create_crud_router(
    repository=CRUDRepository(BatteryStatus, "battery_status_id"),
    create_schema=BatteryStatusCreate,
    read_schema=BatteryStatusRead,
    update_schema=BatteryStatusUpdate,
    resource_name="Battery status record",
    id_path_name="battery_status_id",
)
