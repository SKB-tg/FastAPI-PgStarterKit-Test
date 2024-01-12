from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase, ModelType
from app.models.vakancy import Vakancy
from app.schemas.vakancy import VakancyCreate, VakancyUpdate


class CRUDVakancy(CRUDBase[Vakancy, VakancyCreate, VakancyUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: VakancyCreate, owner_id: int
    ) -> Vakancy:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Vakancy]:
        return (
            db.query(self.model)
            .filter(Vakancy.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_id_vakancy(self, db: Session, id_vakancy: int)-> ModelType:
        return db.query(self.model).filter(self.model.id_vakancy == id_vakancy).first()

    def convert_schemas_to_model(self, obj_in: VakancyCreate
    ) -> Vakancy:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=1)
        return db_obj

vakancy = CRUDVakancy(Vakancy)
