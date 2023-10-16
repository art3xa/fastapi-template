from fastapi import HTTPException

from src.app.internal.core.auth.dto import TokensDTO
from src.app.internal.core.auth.hash import get_password_hash, verify_password
from src.app.internal.core.auth.middlewares.auth import JWTAuth, TokenType
from src.app.internal.core.auth.middlewares.utils import try_decode_token
from src.app.internal.core.auth.models import JWTToken
from src.app.internal.core.auth.repositories import JWTTokenRepository
from src.app.internal.core.auth.utils import generate_device_id
from src.app.internal.users.models import User
from src.app.internal.users.repositories import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository, jwt_token_repo: JWTTokenRepository, jwt_auth: JWTAuth) -> None:
        self.user_repo = user_repo
        self.jwt_token_repo = jwt_token_repo
        self.jwt_auth = jwt_auth

    async def register(self, email: str, password: str) -> TokensDTO:
        if await self.user_repo.get_by_email(email=email):
            raise HTTPException(
                status_code=400,
                detail="Account already exists",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await self.user_repo.create(email=email, hashed_password=get_password_hash(password))
        access_token, refresh_token = await self._issue_tokens(user=user)

        return TokensDTO(access_token=access_token, refresh_token=refresh_token)

    async def login(self, email: str, password: str) -> TokensDTO:
        user = await self.user_repo.get_by_email(email=email)

        if not user:
            raise HTTPException(status_code=400, detail="User not found", headers={"WWW-Authenticate": "Bearer"})
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password", headers={"WWW-Authenticate": "Bearer"})

        access_token, refresh_token = await self._issue_tokens(user=user)

        return TokensDTO(access_token=access_token, refresh_token=refresh_token)

    async def logout(self, user: User, device_id: str) -> None:
        await self.jwt_token_repo.update_by_user_id_and_device_id(
            user_id=user.id, device_id=device_id, is_blacklisted=True
        )

    async def refresh_tokens(self, user: User, refresh_token: str) -> TokensDTO:
        payload, error = try_decode_token(jwt_auth=self.jwt_auth, token=refresh_token)

        if error:
            raise HTTPException(status_code=400, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})

        if payload.get("type") != TokenType.REFRESH.value:
            raise HTTPException(status_code=400, detail="Invalid token type", headers={"WWW-Authenticate": "Bearer"})

        if (await self.jwt_token_repo.get_by_jti(jti=payload.get("jti"))).is_blacklisted:
            await self.jwt_token_repo.update_by_user_id(user_id=user.id, is_blacklisted=True)
            raise HTTPException(
                status_code=400, detail="This token already is blacklisted", headers={"WWW-Authenticate": "Bearer"}
            )

        device_id = payload.get("device_id")
        await self.jwt_token_repo.update_by_user_id_and_device_id(
            user_id=user.id, device_id=device_id, is_blacklisted=True
        )
        access_token, refresh_token = await self._issue_tokens(user=user, device_id=device_id)

        return TokensDTO(access_token=access_token, refresh_token=refresh_token)

    async def _issue_tokens(self, user: User, device_id: str = generate_device_id()) -> dict[str, str]:
        access_token, refresh_token = self.jwt_auth.generate_tokens(
            subject=str(user.id), payload={"device_id": device_id}
        )

        raw_jwt_tokens = [self.jwt_auth.decode_token(token) for token in (access_token, refresh_token)]

        for raw_jwt_token in raw_jwt_tokens:
            await self.jwt_token_repo.create(user_id=user.id, jti=raw_jwt_token.get("jti"), device_id=device_id)

        return access_token, refresh_token

    async def get_tokens(self, user: User) -> list[JWTToken]:
        tokens = await self.jwt_token_repo.get_by_user_id(user_id=user.id)
        return tokens
