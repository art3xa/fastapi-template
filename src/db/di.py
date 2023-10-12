from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.settings import get_settings

engine = create_engine(get_settings().postgres_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async_engine = create_async_engine(get_settings().postgres_url, connect_args={"check_same_thread": False})

AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :yield: database session.
    """
    session: AsyncSession = AsyncSessionLocal()

    try:  # noqa: WPS501
        yield session
    finally:
        await session.close()
