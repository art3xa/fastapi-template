from src.app.internal.core.auth.middlewares.auth import JWTAuth
from src.app.internal.core.auth.service import AuthService
from src.app.internal.users.repositories import UserRepository
from src.db.di import get_db
from src.settings import get_settings


def get_auth_service() -> AuthService:
    repo = UserRepository(db_session=get_db())
    jwt_auth = JWTAuth(config=get_settings().jwt_config)
    return AuthService(
        user_repository=repo,
        jwt_auth=jwt_auth,
    )
