from sqlalchemy import select

from app.internal.users.models import User


class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    async def create(self, email: str, hashed_password: str) -> User:
        user = User(email=email, hashed_password=hashed_password)
        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)
        return user

    async def get_by_email(self, email: str) -> User:
        stmt = select(User).where(User.email == email)
        user = await self.db_session.execute(stmt)
        return user.scalar_one_or_none()
