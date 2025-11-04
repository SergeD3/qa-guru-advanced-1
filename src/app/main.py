import uvicorn
import json

from fastapi import FastAPI

from src.app.models.user_model import UserModel
from fastapi_pagination import add_pagination
from src.app.database import users_db
from src.app.routers import status, user

app = FastAPI()
add_pagination(app)
app.include_router(status.router)
app.include_router(user.router)


if __name__ == "__main__":
    with open(file="../test_data/users.json", mode="r") as f:
        users_db.extend(json.load(f))

    for user in users_db:
        UserModel.model_validate(user)

    uvicorn.run(app, host="localhost", port=8002)
