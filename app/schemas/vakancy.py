import re
from typing import Optional
from datetime import date
from pydantic import ConfigDict, BaseModel, field_serializer


# Shared properties
class VakancyBase(BaseModel):
    id_vakancy: int = 1
    name: str = "--"
    kategory: str = "--"
    link: str = "--"
    company: str = "--"
    price: str = "100"
    description_short: str = "--"
    description_full: str = "--"
    date_publikate: str = "--"

# Properties to receive on item creation
class VakancyCreate(VakancyBase):
    pass


# Properties to receive on item update
class VakancyUpdate(VakancyBase):
    pass


# Properties shared by models stored in DB
class VakancyInDBBase(VakancyBase):
    id: int
    id_vakancy: int
    name: str
    kategory: str
    link: str
    company: str
    price: str
    description_short: str
    description_full: str 
    date_publikate: str 
    model_config = ConfigDict(from_attributes=True)

# Properties to return to client
class Vakancy(VakancyInDBBase):
    id_vakancy: int | str
    price: str

    @field_serializer("id_vakancy")
    def serialize_message(self, id_vakancy: int | str, _info):
        return str(id_vakancy)

    @field_serializer("price")
    def serialize_price(self, price: str, _info):
        price.replace("\u202f", " ")
        return price

# Properties properties stored in DB
class VakancyInDB(VakancyInDBBase):
    pass
