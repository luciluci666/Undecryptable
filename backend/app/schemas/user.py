from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str or None = None


class CreateUser(User):
    name: str
    last_name: str


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None
