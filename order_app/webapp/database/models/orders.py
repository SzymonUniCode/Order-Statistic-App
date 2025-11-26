from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from webapp.extensions import db, migrate

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .order_details import OrderDetail

class Order(db.Model):   # type: ignore
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    order_details: Mapped['OrderDetail'] = relationship(back_populates='order')

    def __repr__(self):
        return f"<Order(id={self.id} User(id={self.user_id})>"