from webapp.services.storage.dtos import ModifyStorageDTO, ReadStorageDTO
from webapp.api.storage.schemas import StorageResponseSchema, ModifyStorageSchema


def to_schema_storage_response(dto: ReadStorageDTO) -> StorageResponseSchema:
    return StorageResponseSchema(
        sku=dto.sku,
        quantity=dto.quantity
    )


def to_dto_modify_storage(schema: ModifyStorageSchema) -> ModifyStorageDTO:
    return ModifyStorageDTO(sku=schema.sku, quantity=schema.quantity)


