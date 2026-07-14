"""API router for alert resources."""

from app.crud import CRUDRepository
from app.models import Alert
from app.routers.crud import create_crud_router
from app.schemas import AlertCreate, AlertRead, AlertUpdate


router = create_crud_router(
    repository=CRUDRepository(Alert, "alert_id"),
    create_schema=AlertCreate,
    read_schema=AlertRead,
    update_schema=AlertUpdate,
    resource_name="Alert",
    id_path_name="alert_id",
)
