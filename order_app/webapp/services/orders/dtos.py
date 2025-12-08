from dataclasses import dataclass
from typing import List



@dataclass(frozen=True)
class ReadOrderDetailDTO:
    sku: str
    qty: int


@dataclass(frozen=True)
class ReadOrderDTO:
    id: int
    user_name: str
    details: List[ReadOrderDetailDTO]



@dataclass(frozen=True)
class CreateOrderDetailDTO:
    sku: str
    qty: int

@dataclass(frozen=True)
class CreateOrderDTO:
    user_name: str
    details: List[CreateOrderDetailDTO]


@dataclass(frozen=True)
class DeleteProductsInOrderDTO:
    order_id: int
    product_sku: str
