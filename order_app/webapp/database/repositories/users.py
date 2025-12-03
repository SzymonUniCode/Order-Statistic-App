from sqlalchemy.orm import selectinload

from webapp.extensions import db
from webapp.database.repositories.generic import GenericRepository
from webapp.database.models.users import User
from sqlalchemy import select

class UserRepository(GenericRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)

    def get_all(self) -> list[User]:
        stmt = select(User).options(selectinload(User.orders))
        return list(db.session.scalars(stmt).all())

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username).options(selectinload(User.orders))
        return db.session.scalar(stmt)


