from typing import Any, Union
from fastapi.responses import (
    PlainTextResponse)
from fastapi import APIRouter, Depends, HTTPException
#from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps

from app.service import parse_data_vacancy, ParserData

router = APIRouter()


@router.post("/quere-new-vakamcy/", response_model=schemas.Vakancy)
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

# @router.get("/{info}")
# def get_vakamcy_info(
#     info: str,
#     db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     info=chat_id&bot_token.
#     """
#     data: dict = {"chat_id": info.replace('&', ",")[0], "bot_token": info.replace('&', ",")[1]}
#     parse_data_vacancy(db, data=data, owner_id=current_user.id)
#     return {"msg": "Ok"}

@router.get("/status")
def get_status(
) -> Any:
    """
    info=chat_id&bot_token.
    """
    return {"msg": "Ok"}

@router.get("/{col}", response_model=schemas.Vakancy)
def get_vacancy_col(
    *,
    db: Session = Depends(deps.get_db),
    col: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    item = crud.vakancy.get_col(db=db, col=col)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (vakancy.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item
