from jose import JWTError

from src.app.internal.core.auth.middlewares.auth import JWTAuth


def try_decode_token(jwt_auth: JWTAuth, token: str) -> tuple[dict, None] | tuple[None, JWTError]:
    try:
        payload = jwt_auth.verify_token(token)
        return payload, None
    except JWTError as error:
        return None, error
