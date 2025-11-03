from pydantic import BaseModel


class AppStatusModel(BaseModel):
    users: bool
