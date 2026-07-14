"""API router for user resources."""

from hashlib import sha256
from typing import Any

from app.crud import CRUDRepository
from app.models import User
from app.routers.crud import create_crud_router
from app.schemas import UserCreate, UserRead, UserUpdate


def prepare_user_create(data: dict[str, Any]) -> dict[str, Any]:
    """Convert a plain password field into the database password_hash field."""
    password = data.pop("password")
    data["password_hash"] = sha256(password.encode("utf-8")).hexdigest()
    return data


def prepare_user_update(data: dict[str, Any]) -> dict[str, Any]:
    """Convert an optional plain password update into password_hash."""
    password = data.pop("password", None)
    if password is not None:
        data["password_hash"] = sha256(password.encode("utf-8")).hexdigest()

    return data


router = create_crud_router(
    repository=CRUDRepository(User, "user_id"),
    create_schema=UserCreate,
    read_schema=UserRead,
    update_schema=UserUpdate,
    resource_name="User",
    id_path_name="user_id",
    create_transform=prepare_user_create,
    update_transform=prepare_user_update,
)
