import json
import dotenv
import pytest
import os
import httpx


@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="module")
def fill_test_data(app_url):
    with open("src/test_data/users.json") as file:
        test_data_users = json.load(file)

    api_users: list = []

    for user in test_data_users:
        response = httpx.post(f"{app_url}/api/users/", json=user)
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        httpx.delete(f"{app_url}/api/users/{user_id}")


@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL")


@pytest.fixture
def get_users(fill_test_data, app_url) -> dict:
    get_response = httpx.get(f"{app_url}/api/users/")

    return get_response.json()