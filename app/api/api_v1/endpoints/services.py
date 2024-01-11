from typing import Any
from fastapi.responses import (
    JSONResponse)
from fastapi import APIRouter, Depends
#from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps

from app.service import parse_data_vacancy, ParserData

router = APIRouter()


@router.post("/quere-new-vakamcy/", response_model=JSONResponse):  #chemas.Vakancy)
def quere_new_vakamcy(
    data: dict,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    #data_in = ParserData(**data)
    data_out = parse_data_vacancy(db, data=ParserData(**data), owner_id=current_user.id)
    print(data_out)
    if data == None:
        return {"msg": "None html"}
    return data_out

@router.get("/{info}")
def get_new_vakamcy(
    info: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    info=chat_id&bot_token.
    """
    data: dict = {"chat_id": info.replace('&')[0], "bot_token": info.replace('&')[1]}
    parse_data_vacancy(data=data, owner_id=current_user.id)
    return {"msg": "Ok"}

@router.get("/status")
def get_status(
) -> Any:
    """
    info=chat_id&bot_token.
    """
    return {"msg": "Ok"}
