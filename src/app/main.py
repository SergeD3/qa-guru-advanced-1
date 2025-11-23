import dotenv

dotenv.load_dotenv()

import uvicorn
from fastapi import FastAPI
from src.app.database.engine import create_db_and_tables
from fastapi_pagination import add_pagination
from src.app.routers import status, user

app = FastAPI()
add_pagination(app)
app.include_router(status.router)
app.include_router(user.router)


if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run(app, host="localhost", port=8002)
