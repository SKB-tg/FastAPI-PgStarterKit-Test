from typing import Any, Union
from fastapi.responses import (
    PlainTextResponse)
from fastapi import APIRouter, Depends, HTTPException, exceptions
#from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app import crud, models, schemas
from app.api import deps

from app.service import parse_data_vacancy, ParserData

router = APIRouter()


@router.post("/quere-new-vakamcy/", response_model=[schemas.VakancyExt])
async def quere_new_vakamcy(
    data: dict,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    #data_in = ParserData(**data)
    try:
        data_out = parse_data_vacancy(db, data=ParserData(**data), owner_id=current_user.id)
        #data_enc = jsonable_encoder(data_out)
        #print(28, data_out.kategory, data_out.name, data_out.id_vakancy, data_out.company,
            data_out.price, data_out.description_short)
        if data == None:
            return {"msg": "None html"}
    except exceptions.ResponseValidationError as error:
        return JSONResponse(status_code=error.status_code, content={"detail": error.detail})
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
    item = crud.vakancy.get_col(db=db, id_vakancy=col)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (vakancy.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item
