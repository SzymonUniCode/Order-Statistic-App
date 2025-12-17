from pydantic import BaseModel, Field

class StorageResponseSchema(BaseModel):
    sku: str
    quantity: int


class ModifyStorageSchema(BaseModel):
    sku: str = Field(min_length=3)
    quantity: int = Field(gt=0)
