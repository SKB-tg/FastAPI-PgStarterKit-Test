from typing import Optional
from datetime import date
from pydantic import ConfigDict, BaseModel


# Shared properties
class VakancyBase(BaseModel):
    id_vakancy: int = 1
    name: str = "--"
    kategory: str = "--"
    link: str = "--"
    company: str = "--"
    price: int = 100
    description_short: str = "--"
    description_full: str = "--"
    date_publikate: date = None

# Properties to receive on item creation
class VakancyCreate(VakancyBase):
    pass


# Properties to receive on item update
class VakancyUpdate(VakancyBase):
    pass


# Properties shared by models stored in DB
class VakancyInDBBase(VakancyBase):
    id_vakancy: int
    name: str
    kategory: str
    link: str
    company: str
    price: int
    description_short: str
    description_full: str 
    date_publikate: Date 


# Properties to return to client
class Vakancy(VakancyInDBBase):
    pass


# Properties properties stored in DB
class VakancyInDB(VakancyInDBBase):
    pass
