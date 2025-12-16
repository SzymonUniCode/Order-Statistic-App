from webapp.extensions import db
from webapp.database.models.storage import Storage
from webapp.database.repositories.storage import StorageRepository
from webapp.database.repositories.products import ProductRepository

from webapp.services.storage.dtos import ReadStorageDTO, ModifyStorageDTO
from webapp.services.storage.mappers import storage_to_dto

from webapp.services.exceptions import NotFoundException, ProductAlreadyExistsException, ServiceException



class StorageService:
    def __init__(self, storage_repo: StorageRepository, product_repo: ProductRepository):
        self.storage_repo = storage_repo
        self.product_repo = product_repo

# ---------------------------------------------------------------------------------------
# Read methods
# ---------------------------------------------------------------------------------------

    def get_all(self) -> list[ReadStorageDTO]:
        stmt = self.storage_repo.get_all()
        return [storage_to_dto(s) for s in stmt]

    def get_by_sku(self, sku: str) -> ReadStorageDTO | None:
        stmt = self.storage_repo.get_by_sku(sku)
        if stmt is None:
            raise NotFoundException(f'Product {sku} not found in storage')
        return storage_to_dto(stmt) if stmt else None



    def get_by_qty_between(self, min_qty: int, max_qty: int) -> list[ReadStorageDTO]:
        stmt = self.storage_repo.get_by_qty_between(min_qty, max_qty)
        if len(stmt) == 0:
            raise NotFoundException(f'Product with qty between {min_qty} and {max_qty} not found in storage')
        return [storage_to_dto(s) for s in stmt]

# ---------------------------------------------------------------------------------------
# Modify methods
# ---------------------------------------------------------------------------------------

    def add_product_to_storage(self, dto: ModifyStorageDTO) -> str:
        with db.session.begin():
            self._check_is_sku_free(dto.sku)
            storage = Storage(sku=dto.sku, qty=dto.quantity)
            self.storage_repo.add(storage)
        return f'Product {dto.sku} added to storage with qty {dto.quantity}'




    def add_qty_to_storage_sku(self, dto: ModifyStorageDTO) -> str:
        with db.session.begin():
            storage_product = self._ensure_product(dto.sku)
            storage_product.qty += dto.quantity
        return f'{dto.quantity} added to {storage_product.sku}'


    def deduct_qty_from_storage_sku(self, dto: ModifyStorageDTO) -> str:
        with db.session.begin():
            storage_product = self._ensure_product(dto.sku)
            if storage_product.qty < dto.quantity:
                raise ServiceException(f'Product {storage_product.sku} cannot have negative qty')
            storage_product.qty -= dto.quantity
        return f'{dto.quantity} deduct from {storage_product.sku}'


    def delete_storage_sku(self, sku: str) -> str:
        with db.session.begin():
            storage = self._ensure_product(sku)
            if storage.qty != 0:
                raise ServiceException(f'Product with left qty cannot be deleted.')
            self.storage_repo.delete_by_id(sku)
        return f'Product {sku} deleted from storage'



# ---------------------------------------------------------------------------------------
# Privet methods
# ---------------------------------------------------------------------------------------

    def _ensure_product(self, sku: str) -> Storage:
        product = self.product_repo.get_by_sku(sku)
        if product is None:
            raise NotFoundException(f'Product {sku} not found in system. Add to products first.')

        storage_product = self.storage_repo.get_by_sku(sku)
        if storage_product is None:
            raise NotFoundException(f'Product {sku} not found. Add to storage')

        return storage_product


    def _check_is_sku_free(self, sku: str) -> None:
        if self.product_repo.get_by_sku(sku) is None:
            raise NotFoundException(f'Product {sku} not found in system. Add to products first.')
        if self.storage_repo.get_by_sku(sku) is not None:
            raise ProductAlreadyExistsException(f'Product {sku} already exists in storage')



