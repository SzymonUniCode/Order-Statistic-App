from webapp.extensions import db
from webapp.database.repositories.generic import GenericRepository
from webapp.database.models.storage import Storage
from sqlalchemy import select


class StorageRepository(GenericRepository[Storage]):
    def __init__(self) -> None:
        super().__init__(Storage)

    def get_by_sku(self, sku: str) -> list[Storage] | None:
        stmt = select(Storage).where(Storage.sku == sku)
        return list(db.session.scalars(stmt).all())

    def get_by_qty_between(self, min_qty: int = 0, max_qty: int = 9999) -> list[Storage] | None:
        stmt = select(Storage).where(Storage.qty >= min_qty, Storage.qty <= max_qty)
        return list(db.session.scalars(stmt).all())