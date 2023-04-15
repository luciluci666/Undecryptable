from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
import os

from app.models import User
from app.utils import Encrypter
from app.utils import ENGINE


Sessionmaker = sessionmaker(bind=ENGINE)
Session = Sessionmaker()

encrypter = Encrypter()


def get_user_by_username(session, username: str):
    user = session.query(User).filter(User.username == username).first()
    session.close()
    return user


def create_user(
    session,
    username: str,
    password: str,
    secret_key_expire_setting: int = 10,
    super_secret_key_expire_setting: int = 30,
) -> User:
    existing_user = session.query(User).filter(User.username == username).first()
    if existing_user:
        raise ValueError("Username already registered")

    hashed_password = encrypter.hash_secret_key(password)
    secret_key_expire = datetime.utcnow() + timedelta(minutes=secret_key_expire_setting)
    super_secret_key_expire = datetime.utcnow() + timedelta(minutes=super_secret_key_expire_setting)

    new_user = User(
        username=username,
        password=hashed_password,
        secret_key_expire_setting=secret_key_expire_setting,
        super_secret_key_expire_setting=super_secret_key_expire_setting,
        secret_key_expire=secret_key_expire,
        super_secret_key_expire=super_secret_key_expire,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user
