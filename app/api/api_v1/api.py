from fastapi import APIRouter
from typing import Any

from app.api.api_v1.endpoints import items, login, users, utils, vakancies, services

api_router = APIRouter()
    
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(vakancies.router, prefix="/vakancies", tags=["vakancies"])
api_router.include_router(services.router, prefix="/services", tags=["services"])

