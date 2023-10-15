from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.users.repositories import UserRepository
from app.internal.users.service import UserService
from db.di import get_db


async def get_user_service(db_session: Annotated[AsyncSession, Depends(get_db)]) -> UserService:
    user_repo = UserRepository(db_session=db_session)
    return UserService(user_repo=user_repo)
