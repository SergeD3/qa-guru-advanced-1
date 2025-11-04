import pytest
import httpx

from http import HTTPStatus
from src.app.models.pagination_model import PaginationModel


class TestUserPagination:
    """Класс с тестами для проверки пагинации для эндпоинта users"""

    def test_users_base_pagination(self, app_url):
        expected_item_number: int = 12
        expected_pages_number: int = 1

        get_response = httpx.get(f"{app_url}/api/users/")

        response_body = get_response.json()
        PaginationModel.model_validate(response_body)

        assert (
                get_response.status_code == HTTPStatus.OK
                and response_body['pages'] == expected_pages_number
                and len(response_body['items']) == expected_item_number
        )

    @pytest.mark.parametrize("size, expected_number", [
        [1, 12],
        [2, 6],
        [3, 4],
        [4, 3],
        [5, 3],
        [6, 2],
        [12, 1]
    ])
    def test_users_size_pagination(self, app_url, size: int, expected_number: int):
        get_response = httpx.get(f"{app_url}/api/users/?size={size}")

        response_body = get_response.json()
        PaginationModel.model_validate(response_body)

        assert (
                get_response.status_code == HTTPStatus.OK
                and response_body['pages'] == expected_number
                and len(response_body["items"]) == size
        )

    @pytest.mark.parametrize("page, expected_number, expected_pages", [
        [1, 6, 2],
        [2, 6, 2],
        [3, 0, 2],
    ])
    def test_users_page_pagination(
            self,
            app_url,
            page: int,
            expected_number: int,
            expected_pages: int
    ):
        get_response = httpx.get(f"{app_url}/api/users?size=6&page={page}")

        response_body = get_response.json()
        PaginationModel.model_validate(response_body)

        assert (
                get_response.status_code == HTTPStatus.OK
                and response_body["page"] == page
                and len(response_body["items"]) == expected_number
        )

    @pytest.mark.parametrize("page, size, expected_item_number", [
        [1, 5, 5],
        [1, 12, 12],
        [2, 5, 5],
        [2, 10, 2],
        [2, 12, 0],
        [3, 5, 2],
        [3, 4, 4],
        [12, 1, 1],
    ])
    def test_users_page_pagination(
            self,
            app_url,
            page: int,
            size: int,
            expected_item_number: int,
    ):
        get_response = httpx.get(f"{app_url}/api/users/?size={size}&page={page}")

        response_body = get_response.json()
        PaginationModel.model_validate(response_body)

        assert (
                get_response.status_code == HTTPStatus.OK
                and response_body["page"] == page
                and response_body["size"] == size
                and len(response_body["items"]) == expected_item_number
        )
