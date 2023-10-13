from fastapi import HTTPException

from src.app.internal.core.auth.dto import TokensDTO
from src.app.internal.core.auth.hash import get_password_hash, verify_password
from src.app.internal.core.auth.middlewares.auth import JWTAuth, TokenType
from src.app.internal.core.auth.middlewares.utils import try_decode_token
from src.app.internal.users.models import User
from src.app.internal.users.repositories import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository, jwt_auth: JWTAuth):
        self.user_repository = user_repository
        self.jwt_auth = jwt_auth

    async def register(self, email: str, password: str) -> None:
        if await self.user_repository.get_by_email(email=email):
            raise HTTPException(status_code=400, detail="This email is already occupied")

        user = await self.user_repository.create(email=email, hashed_password=get_password_hash(password))
        access_token, refresh_token = await self._issue_tokens(user=user)

        return TokensDTO(access_token=access_token, refresh_token=refresh_token)

    async def login(self, email: str, password: str) -> None:
        user = await self.user_repository.get_by_email(email=email)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password")

        access_token, refresh_token = await self._issue_tokens(user=user)

        return TokensDTO(access_token=access_token, refresh_token=refresh_token)

    async def refresh_tokens(self, user: User, refresh_token: str) -> None:
        payload, error = try_decode_token(jwt_auth=self.jwt_auth, token=refresh_token)

        if error:
            raise HTTPException(status_code=400, detail="Invalid token")

        if payload.get("type") != TokenType.REFRESH.value:
            raise HTTPException(status_code=400, detail="Invalid token type")

        access_token, refresh_token = await self._issue_tokens(user=user)

        return TokensDTO(access_token=access_token, refresh_token=refresh_token)

    async def _issue_tokens(self, user: User) -> dict[str, str]:
        access_token = self.jwt_auth.generate_access_token(subject=str(user.id), payload={})
        refresh_token = self.jwt_auth.generate_refresh_token(subject=str(user.id), payload={})
        return access_token, refresh_token
