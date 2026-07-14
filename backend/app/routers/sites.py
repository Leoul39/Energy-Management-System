"""API router for site resources."""

from app.crud import CRUDRepository
from app.models import Site
from app.routers.crud import create_crud_router
from app.schemas import SiteCreate, SiteRead, SiteUpdate


router = create_crud_router(
    repository=CRUDRepository(Site, "site_id"),
    create_schema=SiteCreate,
    read_schema=SiteRead,
    update_schema=SiteUpdate,
    resource_name="Site",
    id_path_name="site_id",
)
