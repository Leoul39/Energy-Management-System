"""Factory for standard CRUD API routers."""

from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.crud.base import CRUDRepository
from app.database import get_db_session

PayloadTransform = Callable[[dict[str, Any]], dict[str, Any]]


def raise_database_error(exc: SQLAlchemyError) -> None:
    """Convert unexpected database failures into a clear API error."""
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Database is unavailable or not configured correctly. Check DATABASE_URL and PostgreSQL.",
    ) from exc


def create_crud_router(
    *,
    repository: CRUDRepository[Any],
    create_schema: type[BaseModel],
    read_schema: type[BaseModel],
    update_schema: type[BaseModel],
    resource_name: str,
    id_path_name: str,
    create_transform: PayloadTransform | None = None,
    update_transform: PayloadTransform | None = None,
) -> APIRouter:
    """Build a standard CRUD router for one SQLAlchemy resource."""
    router = APIRouter()

    @router.get("/", response_model=list[read_schema])
    def list_records(
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=100, ge=1, le=500),
        db_session: Session = Depends(get_db_session),
    ) -> list[Any]:
        """Return a paginated list of records."""
        try:
            return repository.list(db_session, skip=skip, limit=limit)
        except SQLAlchemyError as exc:
            raise_database_error(exc)

    @router.get("/{record_id}", response_model=read_schema)
    def get_record(record_id: int, db_session: Session = Depends(get_db_session)) -> Any:
        """Return one record by primary key."""
        try:
            record = repository.get(db_session, record_id)
        except SQLAlchemyError as exc:
            raise_database_error(exc)

        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{resource_name} not found.",
            )

        return record

    @router.post("/", response_model=read_schema, status_code=status.HTTP_201_CREATED)
    def create_record(
        payload: create_schema,
        db_session: Session = Depends(get_db_session),
    ) -> Any:
        """Create a new record."""
        data = payload.model_dump()
        if create_transform is not None:
            data = create_transform(data)

        try:
            return repository.create(db_session, data)
        except IntegrityError as exc:
            db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{resource_name} could not be created. Check foreign keys and unique fields.",
            ) from exc
        except SQLAlchemyError as exc:
            db_session.rollback()
            raise_database_error(exc)

    @router.patch("/{record_id}", response_model=read_schema)
    def update_record(
        record_id: int,
        payload: update_schema,
        db_session: Session = Depends(get_db_session),
    ) -> Any:
        """Partially update an existing record."""
        try:
            record = repository.get(db_session, record_id)
        except SQLAlchemyError as exc:
            raise_database_error(exc)

        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{resource_name} not found.",
            )

        update_data = payload.model_dump(exclude_unset=True)
        if update_transform is not None:
            update_data = update_transform(update_data)

        try:
            return repository.update(db_session, record, update_data)
        except IntegrityError as exc:
            db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{resource_name} could not be updated. Check constraints and relationships.",
            ) from exc
        except SQLAlchemyError as exc:
            db_session.rollback()
            raise_database_error(exc)

    @router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_record(record_id: int, db_session: Session = Depends(get_db_session)) -> None:
        """Delete one record by primary key."""
        try:
            record = repository.get(db_session, record_id)
        except SQLAlchemyError as exc:
            raise_database_error(exc)

        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{resource_name} not found.",
            )

        try:
            repository.delete(db_session, record)
        except SQLAlchemyError as exc:
            db_session.rollback()
            raise_database_error(exc)

    return router
