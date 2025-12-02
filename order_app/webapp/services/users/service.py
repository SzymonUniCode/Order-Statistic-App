from webapp.extensions import db
from webapp.database.models.users import User
from webapp.database.repositories.users import UserRepository

from webapp.services.users.dtos import CreateUSerDTO, ReadUserDTO
from webapp.services.users.mappers import user_to_dto


class UserService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo


# ---------------------------------------------------------------------------------------
# Read methods
# ---------------------------------------------------------------------------------------

    def get_all(self) -> list[ReadUserDTO]:
        users = self.user_repo.get_all()
        return [user_to_dto(user) for user in users]