from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.internal.core.auth.middlewares.auth import TokenType
from src.app.internal.core.auth.models import JWTToken
from src.app.internal.users.models import User
from src.config.settings import get_settings
from src.db.di import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{get_settings().API_V1_STR}/auth/login")


async def get_current_user(
    request: Request,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """
    Get current user from database.

    :param request: request
    :param token: user token.
    :param db: database session.
    :return: user.
    """
    try:
        payload = jwt.decode(
            token, get_settings().jwt_config.secret_key, algorithms=[get_settings().jwt_config.algorithm]
        )
        if payload.get("type") != TokenType.ACCESS.value:
            raise HTTPException(status_code=403, detail="The passed token does not match the required type")
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="The transferred token is invalid")

    if (await db.get(JWTToken, payload.get("jti"))).is_blacklisted:
        raise HTTPException(status_code=403, detail="The transferred token is blacklisted")

    user = await db.get(User, payload.get("sub"))
    if not user:
        raise HTTPException(status_code=403, detail="The owner of this access token has not been found")
    request.state.device_id = payload.get("device_id")
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Get current active user.

    :param current_user: current user.
    :return: current active user.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_superuser(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    """
    Get current superuser.

    :param current_user: current user.
    :return: current superuser.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="The user does not have enough privileges")
    return current_user
