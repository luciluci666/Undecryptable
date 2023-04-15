from sqlalchemy import Column, Integer, String, DateTime, func
from app.utils.db_config import BASE


class User(BASE):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(64))
    name = Column(String(32))
    last_name = Column(String(32))
    secret_key_expire_setting = Column(Integer, default=60)
    super_secret_key_expire_setting = Column(Integer, default=10)
    secret_key_expire = Column(DateTime(timezone=True))
    super_secret_key_expire = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
