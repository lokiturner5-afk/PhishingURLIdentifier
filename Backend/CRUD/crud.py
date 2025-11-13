from typing import Generic, TypeVar, Type, List, Optional
from database import Base
from sqlalchemy.orm import Session
from pydantic import BaseModel

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model:Type[ModelType]):
        self.model = model

    def get(self, id:int, db:Session) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, db:Session, skip:int= 0, limit:int = 10) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db:Session, obj_in:CreateSchemaType) -> ModelType:
        obj = self.model(**obj_in.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    def update(self, db:Session, obj_in:dict, db_obj:ModelType) -> ModelType:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db:Session, id:int):
        obj = self.get(id, db)
        if obj:
            db.delete(obj)
            db.commit()
        return {'message': f'{obj} has been deleted'}