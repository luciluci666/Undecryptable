from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from app.utils.db_config import BASE


class Password(BASE):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(512))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    application = Column(Integer, ForeignKey("applications.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


class CreditCard(BASE):
    __tablename__ = "credit_cards"

    id = Column(Integer, primary_key=True)
    credit_card_type = Column(String(64), nullable=True)
    cardholder_name = Column(String(64), nullable=True)
    billing_address = Column(String(128), nullable=True)
    last_four_digits = Column(String(4), nullable=False)
    expiration_date = Column(String(7), nullable=False)
    secret_data = Column(String(512), nullable=False)
    application = Column(Integer, ForeignKey("applications.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class SecretData(BASE):
    __tablename__ = "secret_data"

    id = Column(Integer, primary_key=True)
    secret_data = Column(String(512), nullable=False)
    application = Column(Integer, ForeignKey("applications.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
