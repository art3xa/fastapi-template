from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserProfileDTO(BaseModel):
    id: UUID
    email: str

    config = ConfigDict(from_attributes=True)
