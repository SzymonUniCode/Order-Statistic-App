from webapp.extensions import db
from webapp.database.repositories.generic import GenericRepository
from webapp.database.models.products import Product
from sqlalchemy import select
from decimal import Decimal


class ProductRepository(GenericRepository[Product]):
    def __init__(selfself) -> None:
        super().__init__(Product)


    def get_by_part_name(self, product_name: str) -> list[Product]:
        stmt = select(Product).where(Product.name.ilike(f"%{product_name}%"))       #ilike ignore letter size
        return list(db.session.scalars(stmt).all())

    def get_by_price_between(self, min_price: Decimal = Decimal(0.0), max_price: Decimal = Decimal(9999.99)) -> list[Product]:
        stmt = (
            select(Product)
            .where(Product.price >= min_price)
            .where(Product.price <= max_price)
        )

        return list(db.session.scalars(stmt).all())


    def get_by_sku(self, sku: str) -> Product | None:
        stmt = select(Product).where(Product.sku == sku)
        return db.session.scalar(stmt)