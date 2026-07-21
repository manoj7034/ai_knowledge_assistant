from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    # Generic repository with common CRUD operations.

    def __init__(self, db: Session, model: type[ModelType]):
        self.db = db
        self.model = model

    def get(self, entity_id):
        stmt = select(self.model).where(self.model.id == entity_id)
        return self.db.scalar(stmt)

    def get_all(self):
        stmt = select(self.model)
        return list(self.db.scalars(stmt).all())

    def create(self, obj: ModelType):
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelType):
        self.db.delete(obj)
        self.db.commit()