from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.app.internal.core.auth.middlewares.service import get_current_user
from src.app.internal.core.auth.service import AuthService
from src.app.internal.core.auth.transport.di import get_auth_service
from src.app.internal.core.auth.transport.requests import RefreshTokensIn
from src.app.internal.users.models import User

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register")
async def register(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> None:
    """
    Register a new user.

    :param form_data:
    :param auth_service:
    :return:
    """
    res = await auth_service.register(email=form_data.username, password=form_data.password)
    return res


@auth_router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> None:
    """
    Login user.

    :param form_data:
    :param auth_service:
    :return:
    """
    res = await auth_service.login(email=form_data.username, password=form_data.password)
    return res


@auth_router.post("/refresh_tokens")
async def refresh_tokens(
    body: RefreshTokensIn,
    current_user: Annotated[User, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> None:
    """
    Refresh access token.

    :param body:
    :param current_user:
    :param auth_service:
    :return:
    """
    res = await auth_service.refresh_tokens(user=current_user, refresh_token=body.refresh_token)
    return res


@auth_router.post("/me")
async def me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Get current user.

    :param current_user:
    :return:
    """
    return current_user
