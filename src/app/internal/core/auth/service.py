from src.app.internal.core.auth.hash import get_password_hash
from src.app.internal.core.auth.middlewares.auth import JWTAuth
from src.app.internal.users.models import User
from src.app.internal.users.repositories import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository, jwt_auth: JWTAuth):
        self.user_repository = user_repository
        self.jwt_auth = jwt_auth

    async def register(self, email: str, password: str) -> None:
        user = await self.user_repository.create(email=email, hashed_password=get_password_hash(password))
        access_token, refresh_token = await self._issue_tokens(user=user)

        return {"access_token": access_token, "refresh_token": refresh_token}

    async def _issue_tokens(self, user: User) -> dict[str, str]:
        access_token = self.jwt_auth.generate_access_token(subject=str(user.id), payload={})
        refresh_token = self.jwt_auth.generate_refresh_token(subject=str(user.id), payload={})
        return access_token, refresh_token
