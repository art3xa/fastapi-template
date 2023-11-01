import pytest

from src.app.internal.core.auth.middlewares.auth import JWTAuth
from src.config.settings import get_settings


@pytest.fixture()
def jwt_auth():
    return JWTAuth(config=get_settings().jwt_config)
