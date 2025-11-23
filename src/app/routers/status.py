from fastapi import APIRouter
from http import HTTPStatus

from src.app.models.app_status_model import AppStatusModel
from fastapi import HTTPException
from src.app.database.engine import check_db_availability

router = APIRouter()


@router.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatusModel:
    check_result: bool = check_db_availability()

    if not check_result:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail="Service Unavailable")

    return AppStatusModel(database=check_result, status="success", message="The service is available")
