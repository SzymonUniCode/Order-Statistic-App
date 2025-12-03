from dataclasses import dataclass




@dataclass(frozen=True)
class CreateUserDTO:
    name: str


@dataclass(frozen=True)
class ReadUserDTO:
    id: int
    name: str
    orders_qty: int
