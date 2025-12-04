from webapp.extensions import db
from webapp.database.models.users import User
from webapp.database.repositories.users import UserRepository

from webapp.services.users.dtos import CreateUserDTO, ReadUserDTO
from webapp.services.users.mappers import user_to_dto

from webapp.services.exceptions import UserAlreadyExistsException, NotFoundException

class UserService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo


# ---------------------------------------------------------------------------------------
# Read methods
# ---------------------------------------------------------------------------------------

    def get_all(self) -> list[ReadUserDTO]:
        users = self.user_repo.get_all()
        return [user_to_dto(user) for user in users]

    def get_by_username(self, username: str) -> ReadUserDTO | None:
        user = self.user_repo.get_by_username(username)
        return user_to_dto(user) if user else None

# ---------------------------------------------------------------------------------------
# Delete methods
# ---------------------------------------------------------------------------------------

    def delete_user_by_id(self, user_id: int) -> str:
        user = self._get_existing_user(user_id)
        with db.session.begin():
            self.user_repo.delete(user)
        return f"User with id {user_id} deleted successfully."

    def delete_user(self, user: User) -> str:
        self._get_existing_user(user.id)
        with db.session.begin():
            self.user_repo.delete(user)
        return f"User {user.username} deleted successfully."

# ---------------------------------------------------------------------------------------
# Create methods
# ---------------------------------------------------------------------------------------

    def add_user(self, dto: CreateUserDTO):
        with db.session.begin():
            self._check_if_username_free(dto.name)
            user = User(username=dto.name)
            self.user_repo.add(user)
        return user_to_dto(user)




# ---------------------------------------------------------------------------------------
# Privet methods
# ---------------------------------------------------------------------------------------

    def _check_if_username_free(self, username: str) -> None:
        if self.user_repo.get_by_username(username) is not None:
            raise UserAlreadyExistsException(f"User with username {username} already exists.")

    def _get_existing_user(self, user_id: int) -> User:
        user = self.user_repo.get(user_id)
        if user is None:
            raise NotFoundException(f"User with id {user_id} not found.")
        return user