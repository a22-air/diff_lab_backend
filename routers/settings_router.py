from fastapi import APIRouter
from services.settings_service import save_setting, get_settings, delete_setting, update_setting
from schemas.circle_schema import CircleRequest

router = APIRouter()

@router.post("/save")
def save(data: CircleRequest):
    save_setting(data)
    return {"message": "saved"}

@router.get("/settings")
def settings():
    return get_settings()

@router.delete("/settings/{id}")
def delete(id: int):
    delete_setting(id)
    return {"message": "deleted"}

@router.put("/settings/{id}")
def update(id: int, data: CircleRequest):
    update_setting(id, data)
    return {"message": "updated"}