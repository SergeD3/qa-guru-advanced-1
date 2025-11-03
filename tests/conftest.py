import dotenv
import pytest
import os
import httpx

from src.models.user_model import UserModel


@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture
def app_url():
    return os.getenv("APP_URL")


@pytest.fixture
def get_users(app_url) -> list[UserModel]:
    get_response = httpx.get(f"{app_url}/api/users/")

    return get_response.json()