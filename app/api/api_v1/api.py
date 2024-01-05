from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, users, utils, vakancies, services

status = APIRouter()
@status.get("/status")
def get_status(
):
    return {"msg": "Ok"}
  
api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(vakancies.router, prefix="/vakancies", tags=["vakancy"])
api_router.include_router(services.router, prefix="/services", tags=["quere-new-vakamcy"])

