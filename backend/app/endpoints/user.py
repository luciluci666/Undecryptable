from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import os

from app.schemas import User as UserSchema
from app.utils.db_manager import get_user_by_username, create_user, Session
from app.utils import Encrypter, Session


encrypter = Encrypter()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))
JWT_REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_MINUTES"))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User:
    def authenticate_user(username: str, password: str):
        user = get_user_by_username(Session, username)
        if not user:
            return False
        if not encrypter.hash_secret_key(password) == user.password:
            return False
        return user

    def create_access_token(data: dict, expires_delta: timedelta):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    def create_refresh_token(username: str):
        data = {"sub": username}
        expires_delta = timedelta(minutes=JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token = User.create_access_token(data=data, expires_delta=expires_delta)
        return refresh_token

    def get_token(username, password):
        user = User.authenticate_user(username, password)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        access_token = User.create_access_token(
            data={"sub": username}, expires_delta=timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = User.create_refresh_token(username=username)
        return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

    def get_current_user(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user_by_username(Session, username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user

    def register(user: UserSchema):
        existing_user = get_user_by_username(Session, user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        new_user = create_user(Session, user.username, user.password)
        return User.get_token(new_user.username, user.password)

    def login(form_data: OAuth2PasswordRequestForm = Depends()):
        return User.get_token(form_data.username, form_data.password)

    def refresh(refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user_by_username(Session, username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        access_token = User.create_access_token(
            data={"sub": user.username}, expires_delta=timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = User.create_refresh_token(username=user.username)
        return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

    # Define a protected endpoint that requires a valid JWT token
    def protected(user: UserSchema = Depends(get_current_user)):
        return {"username": user.username}
