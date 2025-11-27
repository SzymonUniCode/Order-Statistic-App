from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from webapp.extensions import db

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from .orders import Order

class User(db.Model):   # type: ignore
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)

    orders: Mapped[list["Order"]] = relationship(back_populates="user", lazy="selectin")


    def __repr__(self):
        return f"<User id= {self.id} username='{self.username}'>"


