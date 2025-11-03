from pydantic import BaseModel
from src.models.user_model import UserModel


class PaginationModel(BaseModel):
    size:int
    page: int
    total: int
    pages: int
    items: list[UserModel]
