from pydantic import BaseModel


class TokensDTO(BaseModel):
    access_token: str
    refresh_token: str
