from http import HTTPStatus

from fastapi import HTTPException
from sqlmodel import Session, select
from typing import Iterable
from fastapi_pagination.ext.sqlmodel import paginate
from .engine import engine
from ..models.user_model import UserModel


def get_user(user_id: int) -> UserModel | None:
    with Session(engine) as session:
        return session.get(entity=UserModel, ident=user_id)


def get_users() -> Iterable[UserModel]:
    with Session(engine) as session:
        statement = select(UserModel)
        return session.exec(statement).all()


def get_users_paginated() -> Iterable[UserModel]:
    with Session(engine) as session:
        return paginate(session=session, query=select(UserModel))


def create_user(user: UserModel) -> UserModel:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)

        return user


def delete_user(user_id: int) -> None:
    with Session(engine) as session:
        user = get_user(user_id=user_id)
        session.delete(user)
        session.commit()


def update_user(user_id: int, user: UserModel) -> UserModel | None:
    with Session(engine) as session:
        db_user = get_user(user_id=user_id)

        if not db_user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user
