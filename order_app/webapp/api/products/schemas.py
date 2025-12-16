from pydantic import BaseModel, StringConstraints, Field
from typing_extensions import Annotated
from decimal import Decimal


class CreateProductSchema(BaseModel):
    sku: str = Field(
        min_length=3,
        max_length=10,
        pattern=r'^[a-zA-Z0-9_-]+$'
    )
    name: str = Field(
        min_length=3,
        max_length=90,
        pattern=r'^[a-zA-Z0-9 _-]+$'
    )
    price: Decimal = Field(gt=0, decimal_places=2)


class ProductResponseSchema(BaseModel):
    sku: str
    name: str
    price: Decimal