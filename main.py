import uvicorn
import json
import logging

from fastapi import FastAPI, HTTPException
from http import HTTPStatus

from src.models.user_model import UserModel
from src.models.app_status_model import AppStatusModel


logger = logging.getLogger(__name__)
app = FastAPI()

users: list[UserModel] = []


@app.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatusModel:
    return AppStatusModel(users=bool(users))


@app.get("/api/users/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> UserModel:
    if user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    return users[user_id - 1]


@app.get("/api/users/", status_code=HTTPStatus.OK)
def get_users() -> list[UserModel]:
    return users


if __name__ == "__main__":
    with open(file="src/test_data/users.json", mode="r") as f:
        users = json.load(f)

    for user in users:
        UserModel.model_validate(user)

    logger.info("Пользователи загружены")

    uvicorn.run(app, host="localhost", port=8002)
