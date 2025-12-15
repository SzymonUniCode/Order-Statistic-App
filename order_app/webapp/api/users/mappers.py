from webapp.services.users.dtos import ReadUserDTO, CreateUserDTO
from webapp.api.users.schemas import CreateUserSchema, UserResponseSchema


def to_schemas_read_user(dto: ReadUserDTO) -> UserResponseSchema:
    return UserResponseSchema(
        id=dto.id,
        name=dto.name,
        orders_qty=dto.orders_qty
    )


def to_schemas_user_response():
    pass



