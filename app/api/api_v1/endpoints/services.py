from typing import Any

from fastapi import APIRouter, Depends
#from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps

from app.service import parse_data_vacancy, ParserData

router = APIRouter()


@router.post("/quere-new-vakamcy/", response_model=schemas.Vakancy, status_code=201)
def quere_new_vakamcy(
    data: dict,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    data_out = parse_data_vacancy(data=data, owner_id=current_user.id)
    return {"vakancy": data_out}

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