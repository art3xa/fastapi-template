import uuid

from sqlalchemy import and_, select, update

from src.app.internal.core.auth.models import JWTToken


class JWTTokenRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    async def create(self, user_id: uuid.UUID, jti: str, device_id: str) -> JWTToken:
        jwt_token = JWTToken(jti=jti, user_id=user_id, device_id=device_id)
        self.db_session.add(jwt_token)
        await self.db_session.commit()
        await self.db_session.refresh(jwt_token)
        return jwt_token

    async def get_by_user_id(self, user_id: uuid.UUID) -> JWTToken:
        stmt = select(JWTToken).where(JWTToken.user_id == user_id)
        jwt_tokens = await self.db_session.execute(stmt)
        return jwt_tokens.scalars().all()

    async def get_by_jti(self, jti: str) -> JWTToken:
        jwt_token = await self.db_session.get(JWTToken, jti)
        return jwt_token

    async def update(self, jti: str, **kwargs) -> JWTToken:
        stmt = update(JWTToken).where(JWTToken.jti == jti).values(**kwargs).returning(JWTToken)
        jwt_token = await self.db_session.execute(stmt)
        await self.db_session.commit()
        return jwt_token.scalar_one_or_none()

    async def update_by_user_id(self, user_id: uuid.UUID, **kwargs) -> JWTToken:
        stmt = update(JWTToken).where(JWTToken.user_id == user_id).values(**kwargs)
        await self.db_session.execute(stmt)
        await self.db_session.commit()

    async def update_by_user_id_and_device_id(self, user_id: uuid.UUID, device_id: str, **kwargs) -> None:
        stmt = (
            update(JWTToken)
            .where(and_((JWTToken.user_id == user_id), (JWTToken.device_id == device_id)))
            .values(**kwargs)
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()
