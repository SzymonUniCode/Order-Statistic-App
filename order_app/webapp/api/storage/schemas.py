from pydantic import BaseModel, Field

class StorageResponseSchema(BaseModel):
    sku: str
    quantity: int


class ModifyStorageSchema(BaseModel):
    sku: str
    quantity: int
