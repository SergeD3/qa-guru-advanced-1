from fastapi import APIRouter
from http import HTTPStatus

from src.app.models.app_status_model import AppStatusModel
from fastapi import HTTPException
from src.app.database import users_db

router = APIRouter()


@router.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatusModel:
    if not users_db:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail="Service Unavailable")

    return AppStatusModel(status="success", message="The service is available")
