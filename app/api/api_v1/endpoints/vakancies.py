from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    ORJSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
    StreamingResponse,
    UJSONResponse,
)
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Vakancy])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve items.
    """
    if crud.user.is_superuser(current_user):
        items = crud.vakancy.get_multi(db, skip=skip, limit=limit)
    else:
        items = crud.vakancy.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    print(items.__dict__)
    return items


@router.post("/")#, response_model=schemas.Vakancy)
def create_item_v(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.vakancy.VakancyCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    vakancy = crud.vakancy.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    return vakancy


@router.put("/{id}", response_model=schemas.Vakancy)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.VakancyUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    vakancy = crud.vakancy.get(db=db, id=id)
    if not vakancy:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (vakancy.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    vakancy = crud.vakancy.update(db=db, db_obj=vakancy, obj_in=item_in)
    return vakancy


@router.get("/{id}", response_model=schemas.Vakancy)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    vakancy = crud.vakancy.get(db=db, id=id)
    if not vakancy:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (vakancy.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return vakancy


@router.delete("/{id}", response_model=schemas.Vakancy)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    vakancy = crud.vakancy.get(db=db, id=id)
    if not vakancy:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (vakancy.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    vakancy = crud.vakancy.remove(db=db, id=id)
    return vakancy


@router.get("/{id_vakancy}", response_model=schemas.Vakancy)
def read_vakancy_id(
    *,
    db: Session = Depends(deps.get_db),
    id_vakancy: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    vakancy = crud.vakancy.get_id_vakancy(db=db, id_vakancy=id_vakancy)
    if not vakancy:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (vakancy.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return vakancy
