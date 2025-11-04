from fastapi import APIRouter

from fastapi import HTTPException
from http import HTTPStatus
from fastapi_pagination import Page, paginate

from src.app.models.user_model import UserModel
from src.app.database import users_db

router = APIRouter(prefix="/api/users")


@router.get("/{user_id}", status_code=HTTPStatus.OK, response_model=UserModel)
def get_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    if user_id > len(users_db):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    return users_db[user_id - 1]


@router.get("/", status_code=HTTPStatus.OK, response_model=Page[UserModel])
def get_users():
    return paginate(sequence=users_db)
