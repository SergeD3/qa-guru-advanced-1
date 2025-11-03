import uvicorn
import json
import logging

from fastapi import FastAPI, HTTPException
from http import HTTPStatus

from src.models.user_model import UserModel
from src.models.app_status_model import AppStatusModel
from fastapi_pagination import Page, add_pagination, paginate


logger = logging.getLogger(__name__)
app = FastAPI()
add_pagination(app)

users: list[UserModel] = []


@app.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatusModel:
    if not users:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail="Service Unavailable")

    return AppStatusModel(status="success", message="The service is available")


@app.get("/api/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserModel)
def get_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    return users[user_id - 1]


@app.get("/api/users/", status_code=HTTPStatus.OK, response_model=Page[UserModel])
def get_users():
    return paginate(sequence=users)


if __name__ == "__main__":
    with open(file="src/test_data/users.json", mode="r") as f:
        users = json.load(f)

    for user in users:
        UserModel.model_validate(user)

    uvicorn.run(app, host="localhost", port=8002)
