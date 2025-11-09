from pydantic import BaseModel


class AppStatusModel(BaseModel):
    database: bool
    status: str
    message: str
