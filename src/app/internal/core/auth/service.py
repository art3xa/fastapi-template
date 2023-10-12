from src.app.internal.core.auth.middlewares.auth import JWTAuth
from src.app.internal.users.repositories import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository, jwt_auth: JWTAuth):
        self.user_repository = user_repository
        self.jwt_auth = jwt_auth
