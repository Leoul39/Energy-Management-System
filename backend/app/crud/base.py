"""Reusable CRUD helpers for SQLAlchemy models."""

from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDRepository(Generic[ModelType]):
    """Generic repository for common CRUD database operations."""

    def __init__(self, model: type[ModelType], id_attribute: str) -> None:
        """Store the SQLAlchemy model and its primary-key attribute name."""
        self.model = model
        self.id_attribute = id_attribute

    def list(self, db_session: Session, *, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """Return a paginated list of records."""
        statement = select(self.model).offset(skip).limit(limit)
        return list(db_session.scalars(statement).all())

    def get(self, db_session: Session, record_id: int) -> ModelType | None:
        """Return one record by primary key, or None when it does not exist."""
        return db_session.get(self.model, record_id)

    def create(self, db_session: Session, data: dict[str, Any]) -> ModelType:
        """Create and persist a new record."""
        record = self.model(**data)
        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)
        return record

    def update(
        self,
        db_session: Session,
        record: ModelType,
        data: dict[str, Any],
    ) -> ModelType:
        """Update an existing record with the provided field values."""
        for field_name, value in data.items():
            setattr(record, field_name, value)

        db_session.commit()
        db_session.refresh(record)
        return record

    def delete(self, db_session: Session, record: ModelType) -> None:
        """Delete an existing record."""
        db_session.delete(record)
        db_session.commit()
