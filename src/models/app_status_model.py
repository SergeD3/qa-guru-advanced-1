from pydantic import BaseModel


class AppStatusModel(BaseModel):
    status: str
    message: str
