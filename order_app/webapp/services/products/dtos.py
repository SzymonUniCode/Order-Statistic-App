from dataclasses import dataclass
from decimal import Decimal



@dataclass(frozen=True)
class CreateProductDTO:
    sku: str
    name: str
    price: Decimal

@dataclass(frozen=True)
class ReadProductDTO:
    sku: str
    name: str
    price: Decimal
