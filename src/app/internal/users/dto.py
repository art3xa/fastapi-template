from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserProfileDTO(BaseModel):
    id: UUID
    email: str

    model_config = ConfigDict(from_attributes=True)
