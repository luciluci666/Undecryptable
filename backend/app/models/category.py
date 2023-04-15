from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from app.utils.db_config import BASE


class Category(BASE):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    super_secret = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
