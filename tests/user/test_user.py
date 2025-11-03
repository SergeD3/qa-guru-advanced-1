import pytest
import httpx

from http import HTTPStatus
from src.models.user_model import UserModel


class TestUser:
    @pytest.mark.smoke
    def test_check_status(self, app_url):
        get_response = httpx.get(f"{app_url}/status")

        assert get_response.status_code == HTTPStatus.OK

    def test_get_users(self, app_url):
        get_response = httpx.get(f"{app_url}/api/users/")

        assert get_response.status_code == HTTPStatus.OK

        users = get_response.json()

        for user in users:
            UserModel.model_validate(user)

    @pytest.mark.parametrize("user_id", [1, 6, 12])
    def test_get_user_valid_id(self, app_url, user_id: int):
        get_response = httpx.get(f"{app_url}/api/users/{user_id}")

        assert get_response.status_code == HTTPStatus.OK

        user = get_response.json()

        UserModel.model_validate(user)

    @pytest.mark.parametrize("user_id", [-1, 0, 15, 100])
    def test_cannot_get_user_nonexistent_id(self, app_url, user_id):
        get_response = httpx.get(f"{app_url}/api/users/{user_id}")

        assert get_response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("user_id", ["test", None])
    def test_cannot_get_user_invalid_id(self, app_url, user_id):
        get_response = httpx.get(f"{app_url}/api/users/{user_id}")

        assert get_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


    def test_users_no_duplicates(self, get_users):
        users_ids = [user["id"] for user in get_users]

        assert len(users_ids) == len(set(users_ids))
