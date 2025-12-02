from dataclasses import dataclass




@dataclass(frozen=True)
class CreateUSerDTO:
    id: int
    name: str


@dataclass(frozen=True)
class ReadUserDTO:
    id: int
    name: str
    orders_qty: int
