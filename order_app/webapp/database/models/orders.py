from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from webapp.extensions import db, migrate

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from .order_details import OrderDetail
    from .users import User


class Order(db.Model):   # type: ignore
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"), nullable=False, index=True)

    order_details: Mapped[List['OrderDetail']] = relationship(
        back_populates='order',
        cascade="all, delete-orphan",
        lazy='selectin'
    )


    user: Mapped['User'] = relationship(back_populates='orders', lazy='selectin')

    def __repr__(self):
        return f"<Order id={self.id}, user_id={self.user_id}>"