from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from webapp.extensions import db, migrate


class Storage(db.Model):
    __tablename__ = 'storage'

    sku: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("products.sku"),
        primary_key=True,
        nullable=False
    )

    qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<Storage(sku='{self.sku}', qty={self.qty})>"