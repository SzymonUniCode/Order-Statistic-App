from sqlalchemy import String, CheckConstraint, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from webapp.extensions import db, migrate


from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .order_details import OrderDetail



class Product(db.Model):
    __tablename__ = 'products'

    __table_args__ = (
        CheckConstraint("price >= 0", name="pp_positive_price"),
    )

    sku: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    order_details: Mapped[List['OrderDetail']] = relationship(back_populates='product')


    def __repr__(self):
        return f"<SKU='{self.sku}' name='{self.name}')>"