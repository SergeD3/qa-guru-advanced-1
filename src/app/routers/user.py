from fastapi import APIRouter
from typing import Iterable

from fastapi import HTTPException
from http import HTTPStatus
from fastapi_pagination import Page

from src.app.models.user_model import UserModel, UserCreate, UserUpdate
from src.app.database import users

router = APIRouter(prefix="/api/users")


@router.get(path="/{user_id}", status_code=HTTPStatus.OK, response_model=UserModel)
def get_user(user_id: int) -> UserModel | None:
    if user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)

    user = users.get_user(user_id=user_id)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    return user


@router.get(path="/", status_code=HTTPStatus.OK, response_model=Page[UserModel])
def get_users() -> Iterable[UserModel]:
    return users.get_users_paginated()


@router.post(path="/", status_code=HTTPStatus.CREATED, response_model=UserModel)
def create_user(user: UserModel) -> UserModel:
    UserCreate.model_validate(obj=user.model_dump())

    return users.create_user(user=user)


@router.patch(path="/{user_id}", status_code=HTTPStatus.OK, response_model=UserModel)
def update_user(user_id: int, user: UserModel) -> UserModel:
    if user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)

    UserUpdate.model_validate(obj=user.model_dump())

    return users.update_user(user_id=user_id, user=user)


@router.delete(path="/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int) -> dict[str, str] | None:
    if user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)

    users.delete_user(user_id=user_id)

    return {"message": "User deleted"}