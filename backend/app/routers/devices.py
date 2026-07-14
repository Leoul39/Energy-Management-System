"""API router for device resources."""

from app.crud import CRUDRepository
from app.models import Device
from app.routers.crud import create_crud_router
from app.schemas import DeviceCreate, DeviceRead, DeviceUpdate


router = create_crud_router(
    repository=CRUDRepository(Device, "device_id"),
    create_schema=DeviceCreate,
    read_schema=DeviceRead,
    update_schema=DeviceUpdate,
    resource_name="Device",
    id_path_name="device_id",
)
