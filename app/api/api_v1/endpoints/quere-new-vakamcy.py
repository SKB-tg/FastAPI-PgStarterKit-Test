from typing import Any

from fastapi import APIRouter, Depends
#from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps

from app.service import parse_data_vacancy, ParserData

router = APIRouter()


@router.post("/quere-new-vakamcy/", response_model=schemas.Msg, status_code=201)
def test_email(
    data: ParserData,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    parse_data_vacancy(data=data)
    return {"msg": "Ok"}
