from typing import Annotated

from fastapi import APIRouter, Depends

from src.app.internal.core.auth.middlewares.service import get_current_user
from src.app.internal.users.models import User
from src.app.internal.users.service import UserService
from src.app.internal.users.transport.di import get_user_service
from src.app.internal.users.transport.responses import UserProfileOut

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get(
    path="/me",
    response_model=UserProfileOut,
    status_code=200,
)
async def me(
    current_user: Annotated[User, Depends(get_current_user)],
    users_service: Annotated[UserService, Depends(get_user_service)],
) -> UserProfileOut:
    return users_service.get_me(current_user)


@users_router.get(
    path="/{user_id}",
    response_model=UserProfileOut,
    status_code=200,
)
async def get_user(
    user_id: str,
    users_service: Annotated[UserService, Depends(get_user_service)],
) -> UserProfileOut:
    return await users_service.get_user(user_id)
