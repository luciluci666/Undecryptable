from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from app.utils.db_config import BASE


class Application(BASE):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
