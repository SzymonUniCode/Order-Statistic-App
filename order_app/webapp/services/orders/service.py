from webapp.database.repositories.users import UserRepository
from webapp.extensions import db
from webapp.database.models.orders import Order
from webapp.database.models.order_details import OrderDetail
from webapp.database.repositories.orders import TotalOrderRepository
from webapp.services.orders.dtos import ReadOrderDTO, CreateOrderDTO, CreateOrderDetailDTO
from webapp.services.orders.mappers import order_to_dto, read_dto_order_details_to_order_details
from webapp.services.exceptions import NotFoundException, ProductAlreadyExistsException
from webapp.services.products.service import ProductService
from webapp.services.storage.service import StorageService
from webapp.services.users.service import UserService


class OrderService:
    def __init__(self,
                 order_repo: TotalOrderRepository,
                 user_service: UserService,
                 storage_service: StorageService,
                 product_service: ProductService,
                 ):
        self.order_repo = order_repo
        self.user_service = user_service
        self.storage_service = storage_service
        self.product_service = product_service

# ---------------------------------------------------------------------------------------
# Read methods
# ---------------------------------------------------------------------------------------

    def get_all_orders_with_details(self) -> list[ReadOrderDTO]:
        stmt = self.order_repo.get_all_total_orders()
        return [order_to_dto(o) for o in stmt]


    def get_order_with_details_by_id(self, order_id: int) -> ReadOrderDTO:
        stmt = self.order_repo.get_total_order_by_id(order_id)
        return order_to_dto(stmt)


    def get_all_orders_by_user_name(self, user_name: str) -> list[ReadOrderDTO]:
        self._check_if_user_name_exists(user_name)
        stmt = self.order_repo.get_total_orders_by_user_name(user_name)
        return [order_to_dto(o) for o in stmt]

# ---------------------------------------------------------------------------------------
# Create methods
# ---------------------------------------------------------------------------------------
    # TODO below notes
    # add function that check if qty of product is enough, if not this product in order detail is not added
    # modified qty takes or give qty to qty storage SKU
    # use other services to do it (Product Service and Storage Service)


    #this can add order regulary or with details
    def add_order_with_details(self, dto: CreateOrderDTO) -> None:
        user = self.user_service.get_by_username(dto.user_name)
        if user is None:
            raise NotFoundException(f'User {dto.user_name} not found')

        order_model = Order(
            user_id = user.id,
            order_details=[read_dto_order_details_to_order_details(od) for od in dto.details]
        )

        with db.session.begin():
            self.order_repo.add(order_model)



    def add_product_to_order(self, order_id: int, dto: CreateOrderDetailDTO) -> None:
        with db.session.begin():
            order = self.order_repo.get(order_id)
            if order is None:
                raise NotFoundException(f'Order {order_id} not found')

            for detail in order.order_details:
                if detail.product_sku == dto.sku:
                    raise ProductAlreadyExistsException(f'Product {dto.sku} already exists in this order')

            self.order_repo.add_product_to_order(order, product_sku=dto.sku, qty=dto.qty)

    # TODO below methods

    # update qty in order_details in order

# ---------------------------------------------------------------------------------------
# Delete methods
# ---------------------------------------------------------------------------------------


    # delete order
    # delete product in order



# ---------------------------------------------------------------------------------------
# Privet methods
# ---------------------------------------------------------------------------------------

    def _check_if_user_name_exists(self, user_name: str) -> None:
        if self.user_service.get_by_username(user_name) is None:
            raise NotFoundException(f'{user_name} does not exist')





