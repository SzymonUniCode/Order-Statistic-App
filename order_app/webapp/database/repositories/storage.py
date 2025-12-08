from webapp.extensions import db
from webapp.database.repositories.generic import GenericRepository
from webapp.database.models.storage import Storage
from sqlalchemy import select


class StorageRepository(GenericRepository[Storage]):
    def __init__(self) -> None:
        super().__init__(Storage)

    def get_by_sku(self, sku: str) -> Storage | None:
        stmt = select(Storage).where(Storage.sku == sku)
        return db.session.scalar(stmt)

    def get_by_qty_between(self, min_qty: int = 0, max_qty: int = 9999) -> list[Storage]:
        stmt = (
            select(Storage)
            .where(Storage.qty >= min_qty)
            .where(Storage.qty <= max_qty)
        )
        return list(db.session.scalars(stmt).all())


    def get_by_sku_for_update(self, sku: str) -> Storage | None:
        stmt = (
            select(Storage)
            .where(Storage.sku == sku)
            .with_for_update() # lock the row - avoiding situation where many order will try to update the same product
        )

        return db.session.scalar(stmt)