from src.app.internal.users.dto import UserProfileDTO
from src.app.internal.users.models import User
from src.app.internal.users.repositories import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_me(self, user: User) -> UserProfileDTO:
        return UserProfileDTO.model_validate(user)
