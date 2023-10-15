from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.core.auth.middlewares.auth import JWTAuth
from app.internal.core.auth.repositories import JWTTokenRepository
from app.internal.core.auth.service import AuthService
from app.internal.users.repositories import UserRepository
from config.settings import get_settings
from db.di import get_db


async def get_auth_service(db_session: Annotated[AsyncSession, Depends(get_db)]) -> AuthService:
    user_repo = UserRepository(db_session=db_session)
    jwt_token_repo = JWTTokenRepository(db_session=db_session)
    jwt_auth = JWTAuth(config=get_settings().jwt_config)
    return AuthService(
        user_repo=user_repo,
        jwt_token_repo=jwt_token_repo,
        jwt_auth=jwt_auth,
    )
