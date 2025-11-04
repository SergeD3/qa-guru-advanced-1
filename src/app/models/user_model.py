from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional


class UserModel(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: Optional[HttpUrl]
