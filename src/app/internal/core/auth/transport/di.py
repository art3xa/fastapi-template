from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.internal.core.auth.middlewares.auth import JWTAuth
from src.app.internal.core.auth.service import AuthService
from src.app.internal.users.repositories import UserRepository
from src.db.di import get_db
from src.settings import get_settings


async def get_auth_service(db_session: Annotated[AsyncSession, Depends(get_db)]) -> AuthService:
    repo = UserRepository(db_session=db_session)
    jwt_auth = JWTAuth(config=get_settings().jwt_config)
    return AuthService(
        user_repository=repo,
        jwt_auth=jwt_auth,
    )
