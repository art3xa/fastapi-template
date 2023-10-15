from app.internal.users.dto import UserProfileDTO
from app.internal.users.models import User
from app.internal.users.repositories import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_me(self, user: User) -> UserProfileDTO:
        return UserProfileDTO.model_validate(user)
