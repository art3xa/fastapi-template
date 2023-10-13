from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.settings import get_settings

settings = get_settings()

async_engine = create_async_engine(str(settings.async_postgres_url), echo=settings.DEBUG)

AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Create and get database session.

    :yield: database session.
    """
    async with AsyncSessionLocal() as session:
        yield session
