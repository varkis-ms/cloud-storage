from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from cloud_storage.schemas import RegistrationForm
from cloud_storage.config import get_settings
from cloud_storage.db.connection import get_session
from cloud_storage.db.models import User
from cloud_storage.utils.user.auth_db import *
from cloud_storage.schemas import TokenData


def verify_password(
        plain_password: str,
        hash_password: str
) -> bool:
    return get_settings().PWD_CONTEXT.verify(plain_password, hash_password)


async def authenticate_user(
    session: AsyncSession,
    username: str,
    password: str,
) -> bool | User:
    user = await get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    settings = get_settings()
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(get_settings().OAUTH2_SCHEME),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await get_user(session, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
