from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.app.internal.core.auth.middlewares.service import get_current_user
from src.app.internal.core.auth.service import AuthService
from src.app.internal.core.auth.transport.di import get_auth_service
from src.app.internal.core.auth.transport.requests import RefreshTokensIn
from src.app.internal.core.auth.transport.responses import SuccessOut, TokensOut
from src.app.internal.users.models import User

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    path="/register",
    response_model=TokensOut,
    status_code=201,
)
async def register(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokensOut:
    """
    Register a new user.

    :param form_data:
    :param auth_service:
    :return:
    """
    res = await auth_service.register(email=form_data.username, password=form_data.password)
    return res


@auth_router.post(
    path="/login",
    response_model=TokensOut,
    status_code=200,
)
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


@auth_router.post(
    path="/logout",
    response_model=None,
    status_code=200,
)
async def logout(
    current_user: Annotated[User, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> None:
    await auth_service.logout(user=current_user)
    return SuccessOut()


@auth_router.post(
    path="/refresh_tokens",
    response_model=TokensOut,
    status_code=200,
)
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
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> None:
    tokens = await auth_service.get_tokens(user=current_user)
    return tokens, current_user
