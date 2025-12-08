from sqlalchemy import Integer, ForeignKey, DateTime, func, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from webapp.extensions import db
from datetime import datetime


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .products import Product
    from .orders import Order


class OrderDetail(db.Model):    # type: ignore
    __tablename__ = 'order_details'

    __table_args__ = (
        db.PrimaryKeyConstraint("order_id", "product_sku"),
        db.UniqueConstraint("order_id", "product_sku")
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="cascade"), nullable=False, index=True
    )
    product_sku: Mapped[str] = mapped_column(
        ForeignKey("products.sku", ondelete="cascade"), nullable=False, index=True
    )
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    product: Mapped['Product'] = relationship(back_populates='order_details', lazy='selectin')
    order: Mapped['Order'] = relationship(back_populates='order_details', lazy='selectin')


    def __repr__(self):
        return f"<OrderDetail(order_id={self.order_id}, product_sku={self.product_sku}, qty={self.qty})>"