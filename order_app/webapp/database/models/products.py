from sqlalchemy import String, CheckConstraint, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from webapp.extensions import db
from decimal import Decimal


from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .order_details import OrderDetail
    from .storage import Storage



class Product(db.Model):     # type: ignore
    __tablename__ = 'products'

    __table_args__ = (
        CheckConstraint("price >= 0", name="pp_positive_price"),
    )

    sku: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    order_details: Mapped[List['OrderDetail']] = relationship(
        back_populates='product',
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    storage: Mapped["Storage"] = relationship(
        back_populates="product",
        uselist=False,
        lazy="selectin",
        cascade="all, delete-orphan")


    def __repr__(self):
        return f"<SKU='{self.sku}' name='{self.name}' price={self.price}>"