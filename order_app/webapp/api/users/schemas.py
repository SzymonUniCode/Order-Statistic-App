from pydantic import BaseModel, StringConstraints, Field
from typing_extensions import Annotated



class CreateUserSchema(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=20,
        pattern=r'^[a-zA-Z]+$'
    )


class UserResponseSchema(BaseModel):
    id: int
    name: str
    orders_qty: int