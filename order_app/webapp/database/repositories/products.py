from webapp.extensions import db
from webapp.database.repositories.generic import GenericRepository
from webapp.database.models.products import Product
from sqlalchemy import select


class ProductRepository(GenericRepository[Product]):
    def __init__(selfself) -> None:
        super().__init__(Product)


    def get_by_part_name(self, product_name: str) -> list[Product] | None:
        stmt = select(Product).where(Product.name.ilike(f"%{product_name}%"))       #ilike ignore letter size
        return list(db.session.scalars(stmt).all())

    def get_by_price_between(self, min_price: float = 0.0, max_price: float = 9999.99) -> list[Product] | None:
        stmt = select(Product).where(min_price <= Product.price <= max_price)
        return list(db.session.scalars(stmt).all())