from typing import TypeVar

from pydantic import BaseModel

from src.database import Base

DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

class DataMapper:
    db_model: type[DBModelType] = None #sqlalchemy model
    schema: type[SchemaType] = None #pydantic schema

    @classmethod
    def map_to_domain_entity(cls, data): #model -> schema
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data): #schema -> model
        return cls.db_model(**data.model_dump())