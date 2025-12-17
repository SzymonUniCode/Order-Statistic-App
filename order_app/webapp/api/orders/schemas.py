from typing import List
from pydantic import BaseModel, Field



class OrderDetailsResponseSchema(BaseModel):
    sku: str
    qty: int


class OrderResponseSchema(BaseModel):
    id: int
    user_name: str
    details: List[OrderDetailsResponseSchema]


class CreateOrderDetailSchema(BaseModel):
    sku: str = Field(min_length=3)
    qty: int = Field(gt=0)


class CreateOrderSchema(BaseModel):
    user_name: str
    details: List[CreateOrderDetailSchema]


class DeleteProductInOrderSchema(BaseModel):
    order_id: int
    product_sku: str
