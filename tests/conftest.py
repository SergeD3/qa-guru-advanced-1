import dotenv
import pytest
import os
import httpx


@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture
def app_url():
    return os.getenv("APP_URL")


@pytest.fixture
def get_users(app_url) -> dict:
    get_response = httpx.get(f"{app_url}/api/users/")

    return get_response.json()