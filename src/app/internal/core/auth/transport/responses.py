from pydantic import BaseModel


class TokensOut(BaseModel):
    access_token: str
    refresh_token: str


class SuccessOut(BaseModel):
    success: bool = True
