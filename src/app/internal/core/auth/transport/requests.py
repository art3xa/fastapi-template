from pydantic import BaseModel


class RefreshTokensIn(BaseModel):
    refresh_token: str
