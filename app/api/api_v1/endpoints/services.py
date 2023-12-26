from typing import Any

from fastapi import APIRouter, Depends
#from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps

from app.service import parse_data_vacancy, ParserData

router = APIRouter()


@router.post("/quere-new-vakamcy/", response_model=schemas.Msg, status_code=201)
def quere_new_vakamcy(
    data: ParserData,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    parse_data_vacancy(data=data)
    return {"msg": "Ok"}

@router.get("/{info}")
def get_new_vakamcy(
    info: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    info=chat_id&bot_token.
    """
    data: dict = {"chat_id": info.replace('&')[0], "bot_token": info.replace('&')[1]}
    parse_data_vacancy(data=data)
    return {"msg": "Ok"}