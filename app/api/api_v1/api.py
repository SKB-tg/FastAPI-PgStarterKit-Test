from fastapi import APIRouter
from typing import Any

from app.api.api_v1.endpoints import items, login, users, utils, vakancies, services

api_router = APIRouter()
status_r = APIRouter()
api_router.include_router(status_r)

@status_r.get("/status", status_code=200)
def get_status_r():
    return {"msg": "Ok"}
    
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(vakancies.router, prefix="/vakancies", tags=["vakancy"])
api_router.include_router(services.router, prefix="/services", tags=["quere-new-vakamcy"])

