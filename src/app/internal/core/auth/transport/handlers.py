from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.app.internal.core.auth.service import AuthService
from src.app.internal.core.auth.transport.di import get_auth_service

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
