import pytest
import httpx

from http import HTTPStatus
from src.app.models.user_model import UserModel
from src.app.models.pagination_model import PaginationModel
from src.app.helpers.common_helper import get_random_email, get_random_first_name, get_random_last_name, get_random_url, get_random_number


class TestUser:
    @pytest.mark.smoke
    def test_check_service_status(self, app_url):
        expected_status = "success"

        get_response = httpx.get(f"{app_url}/status")

        response_body = get_response.json()

        assert (
                get_response.status_code == HTTPStatus.OK
                and response_body["status"] == expected_status
        )

    @pytest.mark.smoke
    @pytest.mark.parametrize("test_data", [
        {
            "email": get_random_email(),
            "first_name": get_random_first_name(),
            "last_name": get_random_last_name(),
            "avatar": get_random_url()
        }
    ])
    def test_create_user(self, app_url, test_data: dict[str, str]):
        create_response = httpx.post(url=f"{app_url}/api/users/", json=test_data)

        response_body = create_response.json()

        assert (
            create_response.status_code == HTTPStatus.CREATED
            and response_body["id"] is not None
            and response_body["email"] == test_data["email"]
            and response_body["first_name"] == test_data["first_name"]
            and response_body["last_name"] == test_data["last_name"]
            and response_body["avatar"] == test_data["avatar"]
        )

    @pytest.mark.smoke
    def test_delete_user(self, app_url, fill_test_data):
        expected_user_id = fill_test_data[-1]
        expected_message: str = "User deleted"

        delete_response = httpx.delete(url=f"{app_url}/api/users/{expected_user_id}")

        response_body = delete_response.json()

        assert delete_response.status_code == HTTPStatus.OK and response_body["message"] == expected_message

    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "test_data",
        [
            {
                "email": "update_email@test.ru",
                "first_name": "Update first name",
                "last_name": "Update last name",
                "avatar": "https://update_url.com",
            }
        ],
    )
    def test_update_user(self, app_url, fill_test_data, test_data: dict):
        user_id_for_test = fill_test_data[0]

        update_response = httpx.patch(
            url=f"{app_url}/api/users/{user_id_for_test}", json=test_data
        )

        response_body = update_response.json()

        assert (
            update_response.status_code == HTTPStatus.OK
            and response_body["email"] == test_data["email"]
            and response_body["first_name"] == test_data["first_name"]
            and response_body["last_name"] == test_data["last_name"]
            and response_body["avatar"] == test_data["avatar"]
        )

    @pytest.mark.smoke
    def test_get_users(self, app_url):
        get_response = httpx.get(f"{app_url}/api/users/")

        assert get_response.status_code == HTTPStatus.OK

        users = get_response.json()

        PaginationModel.model_validate(users)

    @pytest.mark.smoke
    def test_get_user_valid_id(self, fill_test_data, app_url):
        response_first_element = httpx.get(f"{app_url}/api/users/{fill_test_data[0]}")

        assert response_first_element.status_code == HTTPStatus.OK

        UserModel.model_validate(response_first_element.json())

    @pytest.mark.parametrize("user_id", [-1, 0])
    def test_cannot_get_user_nonexistent_id(self, app_url, user_id):
        get_response = httpx.get(f"{app_url}/api/users/{user_id}")

        assert get_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("user_id", ["test", None])
    def test_cannot_get_user_invalid_id(self, app_url, user_id):
        get_response = httpx.get(f"{app_url}/api/users/{user_id}")

        assert get_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.smoke
    def test_users_no_duplicates(self, get_users):
        users_ids = [user["id"] for user in get_users["items"]]

        assert len(users_ids) == len(set(users_ids))

    def test_get_user_405_method_not_allowed(self, app_url):
        response_first_element = httpx.post(f"{app_url}/api/users/{1}")

        assert response_first_element.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    @pytest.mark.regression
    def test_delete_user_404_not_found(self, app_url):
        expected_user_id = get_random_number(number_digits=3)

        delete_response = httpx.delete(url=f"{app_url}/api/users/{expected_user_id}")

        assert delete_response.status_code == HTTPStatus.NOT_FOUND
