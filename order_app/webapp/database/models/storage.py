from sqlalchemy import Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from webapp.extensions import db

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .products import Product

class Storage(db.Model):    # type: ignore
    __tablename__ = 'storage'

    __table_args__ = (
        CheckConstraint("qty >= 0", name="st_positive_qty"),
    )

    sku: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("products.sku", ondelete="cascade"),
        primary_key=True,
        nullable=False
    )

    qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    product: Mapped["Product"] = relationship(back_populates="storage", lazy="selectin")

    def __repr__(self):
        return f"<Storage(sku='{self.sku}', qty={self.qty})>"