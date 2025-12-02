from webapp.database.models.users import User
from webapp.services.users.dtos import ReadUserDTO

def user_to_dto(user: User) -> ReadUserDTO:
    return ReadUserDTO(
        id=user.id,
        name=user.username,
        orders_qty=len(user.orders)
    )