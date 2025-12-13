import pytest
import httpx

from http import HTTPStatus
from src.app.models.pagination_model import PaginationModel


class TestUserPagination:
    """Класс с тестами для проверки пагинации для эндпоинта users"""

    def test_users_base_pagination(self, app_url):
        expected_pages_number: int = 1

        get_response = httpx.get(f"{app_url}/api/users/")

        response_body = get_response.json()
        PaginationModel.model_validate(response_body)

        assert get_response.status_code == HTTPStatus.OK
        assert response_body['pages'] == expected_pages_number

    @pytest.mark.parametrize("size", (
        [1, 2, 3, 4, 5]
    ))
    def test_users_size_pagination(self, app_url, size: int):
        get_response = httpx.get(f"{app_url}/api/users/?size={size}")

        response_body = get_response.json()
        PaginationModel.model_validate(response_body)

        assert get_response.status_code == HTTPStatus.OK

    @pytest.mark.parametrize("page", (
        [1, 2, 3]
    ))
    def test_users_page_pagination(
            self,
            app_url,
            page: int,
    ):
        get_response = httpx.get(f"{app_url}/api/users/?size=6&page={page}")

        response_body = get_response.json()
        PaginationModel.model_validate(response_body)

        assert get_response.status_code == HTTPStatus.OK

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
    def test_users_size_page_pagination(
            self,
            app_url,
            page: int,
            size: int,
            expected_item_number: int,
    ):
        get_response = httpx.get(f"{app_url}/api/users/?size={size}&page={page}")

        response_body = get_response.json()
        PaginationModel.model_validate(response_body)

        assert get_response.status_code == HTTPStatus.OK
