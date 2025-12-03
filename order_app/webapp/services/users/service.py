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
        return user_to_dto(user) if user is not None else None

# ---------------------------------------------------------------------------------------
# Delete methods
# ---------------------------------------------------------------------------------------

    def delete_user(self, user: User) -> str:
        if self._check_if_user_exists(user.id) is True:
            with db.session.begin():
                self.user_repo.delete(user)
        return f"User {user.username} deleted successfully."




    def delete_user_by_id(self, id: int) -> str:
        if self._check_if_user_exists(id) is True:
            with db.session.begin():
                self.user_repo.delete_by_id(id)
        return f"User with id {id} deleted successfully."

# ---------------------------------------------------------------------------------------
# Create methods
# ---------------------------------------------------------------------------------------

    def add_user(self, dto: CreateUserDTO):
        with db.session.begin():
            self._check_if_user(dto.name)
            user = User(username=dto.name)
            self.user_repo.add(user)
        return user_to_dto(user)




# ---------------------------------------------------------------------------------------
# Privet methods
# ---------------------------------------------------------------------------------------

    def _check_if_user(self, username: str) -> None:
        user = self.user_repo.get_by_username(username)

        if user is not None:
            raise UserAlreadyExistsException(f"User with username {username} already exists.")
        return None

    def _check_if_user_exists(self, id: int) -> bool:
        if self.user_repo.get(id) is not None:
            return True
        raise NotFoundException(f"User with username {id} not found.")