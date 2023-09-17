from sqlalchemy import Integer
from models import session, metadata, engine
from .models import User
from typing import List



def get_user(username_or_id) -> User:
    if isinstance(username_or_id, int):
        user = get_user_by_id(username_or_id)
    else:
        user = get_user_by_username(username_or_id)
    
    if user is None:
        user = get_user_by_tg_id(username_or_id)
    
    return user


def get_users() -> List[User]:
    return session.query(User).all()


def get_user_by_id(user_id: Integer) -> User:
    return session.query(User).filter(User.id == user_id).first()


def get_user_by_username(username: str) -> User:
    return session.query(User).filter(User.username == username).first()


def get_user_by_tg_id(user_tg_id: int) -> User:
    return session.query(User).filter(User.tg_id == user_tg_id).first()


def get_user_password(user_tg_id: int) -> str:
    user = get_user_by_tg_id(user_tg_id=user_tg_id)
    return user.password


def get_admins() -> List[User]:
    return session.query(User).filter(User.is_admin)


def save_new_user(tg_id: int, username: str, password: str) -> User:
    user = User(tg_id, username, password)
    user.commit()
    return user


def grant_user_admin_role(user: User):
    user.is_admin = True
    user.commit()

metadata.create_all(engine)
