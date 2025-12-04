from dataclasses import dataclass

@dataclass(frozen=True)
class ReadStorageDTO:
    sku: str
    quantity: int


@dataclass(frozen=True)
class ModifyStorageDTO:
    sku: str
    quantity: int
