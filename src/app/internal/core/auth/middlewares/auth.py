from datetime import datetime, timedelta
from enum import Enum, unique
from typing import Any
from uuid import uuid4

from jose import jwt

from src.app.internal.core.auth.utils import convert_to_timestamp
from src.config.settings import JWTConfig


@unique
class TokenType(str, Enum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class JWTAuth:
    """JWTAuth class."""

    def __init__(self, config: JWTConfig) -> None:
        """Initialize the JWTAuth class."""
        self._config = config

    def generate_tokens(self, subject: str, payload: dict[str, Any]) -> tuple[str, str]:
        """Generate access and refresh tokens.

        :param subject: str
        :param payload: dict[str, Any]
        :return: str
        """
        access_token = self.generate_access_token(subject, payload)
        refresh_token = self.generate_refresh_token(subject, payload)
        return access_token, refresh_token

    def __sign_token(self, token_type: TokenType, subject: str, payload: dict[str, Any], ttl: timedelta) -> str:
        """Sign the token.

        :param token_type: TokenType
        :param subject: str
        :param payload: dict[str, Any]
        :param ttl: timedelta
        :return: str
        """
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

    def generate_access_token(self, subject: str, payload: dict[str, Any]) -> str:
        """Generate an access token.

        :param subject: str
        :param payload: dict[str, Any]
        :return: str
        """
        return self.__sign_token(TokenType.ACCESS, subject, payload, self._config.access_token_ttl)

    def generate_refresh_token(self, subject: str, payload: dict[str, Any]) -> str:
        """Generate a refresh token.

        :param subject: str
        :param payload: dict[str, Any]
        :return: str
        """
        return self.__sign_token(TokenType.REFRESH, subject, payload, self._config.refresh_token_ttl)

    def verify_token(self, token: str) -> dict[str, Any]:
        """Verify the token and decode it.

        :param token: str
        :return: dict[str, Any]
        """
        return jwt.decode(token, self._config.secret_key, algorithms=[self._config.algorithm])

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        """Decode the token without verifying the signature.

        :param token: str
        :return: dict[str, Any]
        """
        return jwt.get_unverified_claims(token)
