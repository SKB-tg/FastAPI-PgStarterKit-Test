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
    # id_vakancy: int | str

    # @field_serializer("id_vakancy")
    # def serialize_message(self, id_vakancy: int | str, _info):
    #     return str(id_vakancy)
    pass

# Properties properties stored in DB
class VakancyInDB(VakancyInDBBase):
    pass

class VakancyExt(BaseModel):
    id_vakancy: int | str = 1
    name: str | None = "--"
    kategory: str | None = "--"
    company: str | None = "--"
    price: str | None = "--"
    description_short: str | None = "--"
    date_publikate: str | None = "--"
    mess_id: int | None = 1

    # @field_serializer("id_vakancy")
    # def serialize_message(self, id_vakancy: int | str, _info):
    #     return str(id_vakancy)

    # @field_serializer("name")
    # def serialize_message(self, name: str, _info):
    #     return name
    # @field_serializer("kategory")
    # def serialize_message(self, kategory: str, _info):
    #     return kategory
    # @field_serializer("company")
    # def serialize_message(self, company: str, _info):
    #     return company
    # @field_serializer("price")
    # def serialize_price(self, price: str):
    #     price.replace("\u202f", "%D0%")
    #     price = "OOO"
    #     return price
    #date_publikate: str 
    #model_config = ConfigDict(from_attributes=True)
