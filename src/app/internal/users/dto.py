from uuid import UUID

from pydantic import BaseModel


class UserProfileDTO(BaseModel):
    id: UUID
    email: str

    class Config:
        from_attributes = True
