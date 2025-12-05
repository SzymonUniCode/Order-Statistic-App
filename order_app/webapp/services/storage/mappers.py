from webapp.database.models.storage import Storage
from webapp.services.storage.dtos import ReadStorageDTO


def storage_to_dto(storage: Storage) -> ReadStorageDTO:
    return ReadStorageDTO(
        sku = storage.sku,
        quantity = storage.qty,
    )