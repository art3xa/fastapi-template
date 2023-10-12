from calendar import timegm
from datetime import datetime, timedelta
from enum import Enum, unique
from typing import Any
from uuid import uuid4

from jose import jwt

from src.config.settings import JWTConfig


@unique
class TokenType(str, Enum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


def convert_to_timestamp(datetime: datetime) -> int:
    return timegm(datetime.utctimetuple())


class JWTAuth:
    def __init__(self, config: JWTConfig) -> None:
        self._config = config

    def __sign_token(self, token_type: TokenType, subject: str, payload: dict[str, Any], ttl: timedelta) -> str:
        current_timestamp = convert_to_timestamp(datetime.utcnow())
        data = {
            "iss": self._config.issuer,
            "sub": subject,
            "type": token_type.value,
            "jti": str(uuid4()),
            "iat": current_timestamp,
            "nbf": payload.get("nbf", current_timestamp),
            "exp": (current_timestamp + int(ttl.total_seconds())) if ttl else None,
        }
        payload.update(data)
        return jwt.encode(payload, self._config.secret_key, algorithm=self._config.algorithm)
