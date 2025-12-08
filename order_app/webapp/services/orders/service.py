from webapp.database.repositories.storage import StorageRepository
from webapp.database.repositories.users import UserRepository
from webapp.extensions import db
from webapp.database.models.orders import Order
from webapp.database.models.order_details import OrderDetail
from webapp.database.repositories.orders import TotalOrderRepository
from webapp.services.orders.dtos import ReadOrderDTO, CreateOrderDTO, CreateOrderDetailDTO, DeleteProductsInOrderDTO
from webapp.services.orders.mappers import order_to_dto, read_dto_order_details_to_order_details
from webapp.services.exceptions import NotFoundException, ProductAlreadyExistsException, NotEnoughStockException, \
    ServiceException
from webapp.services.products.service import ProductService
from webapp.services.storage.dtos import ModifyStorageDTO
from webapp.services.storage.service import StorageService
from webapp.services.users.service import UserService


class OrderService:
    def __init__(self,
                 order_repo: TotalOrderRepository,
                 storage_repo: StorageRepository,
                 user_service: UserService,
                 storage_service: StorageService,
                 product_service: ProductService,
                 ):
        self.order_repo = order_repo
        self.storage_repo = storage_repo
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
        if stmt is None:
            raise NotFoundException(f'Order {order_id} not found')
        return order_to_dto(stmt)


    def get_all_orders_by_user_name(self, user_name: str) -> list[ReadOrderDTO]:
        self._check_if_user_name_exists(user_name)
        stmt = self.order_repo.get_total_orders_by_user_name(user_name)
        return [order_to_dto(o) for o in stmt]

# ---------------------------------------------------------------------------------------
# Create methods
# ---------------------------------------------------------------------------------------

    def add_order_with_details(self, dto: CreateOrderDTO) -> None:
        user = self.user_service.get_by_username(dto.user_name)
        if user is None:
            raise NotFoundException(f'User {dto.user_name} not found')

        for item in dto.details:
            self._positive_data_validation(item.sku, item.qty)

        with db.session.begin():
            order = Order(user_id=user.id)
            self.order_repo.add(order)
            db.session.flush() # to have order in DB to go further with the below code

            for detail in dto.details:
                self._add_product_internal(order, detail)


    def add_product_to_order(self, order_id: int, dto: CreateOrderDetailDTO) -> None:
        self._positive_data_validation(dto.sku, dto.qty)

        with db.session.begin():
            order = self.order_repo.get(order_id)
            if order is None:
                raise NotFoundException(f'Order {order_id} not found')

            self._add_product_internal(order, dto)

# ---------------------------------------------------------------------------------------
# Delete methods
# ---------------------------------------------------------------------------------------


    # delete order
    def delete_order_with_details(self, order_id: int) -> None:
        with db.session.begin():
            self.order_repo.delete_by_id(order_id)
            print(f'Order {order_id} deleted with all details')


    def delete_product_in_order(self, dto: DeleteProductsInOrderDTO) -> None:
        with db.session.begin():
            order = self.order_repo.get(dto.order_id)
            if order is None:
                raise NotFoundException(f'Order {dto.order_id} not found')

            detail = next(
                (od for od in order.order_details if od.product_sku == dto.product_sku),
                None
            )

            if detail is None:
                raise NotFoundException(f'Product {dto.product_sku} not found in order {dto.order_id}')


            storage_item = self.storage_repo.get_by_sku_for_update(detail.product_sku)
            if storage_item is None:
                raise NotFoundException(f'Product {dto.product_sku} not found in storage')
            storage_item.qty += detail.qty
            order.order_details.remove(detail)










# ---------------------------------------------------------------------------------------
# Privet methods
# ---------------------------------------------------------------------------------------

    def _check_if_user_name_exists(self, user_name: str) -> None:
        if self.user_service.get_by_username(user_name) is None:
            raise NotFoundException(f'{user_name} does not exist')


    def _positive_data_validation(self, sku: str, qty: int) -> None:
        if qty <= 0:
            raise ServiceException(f'Qty {qty} must be positive')
        if not sku or sku.strip() == '':
            raise ServiceException(f'Product sku {sku} is empty')

    def _add_product_internal(self, order: Order, dto: CreateOrderDetailDTO) -> None:
        for detail in order.order_details:
            if detail.product_sku == dto.sku:
                raise ProductAlreadyExistsException(f'Product {dto.sku} already exists in order {order.id}')

        product_storage = self.storage_repo.get_by_sku_for_update(dto.sku)

        if product_storage is None:
            raise NotFoundException(f'Product {dto.sku} not found in storage')

        if product_storage.qty < dto.qty:
            raise NotEnoughStockException(
                f'Ordered QTY {dto.qty} > Storage QTY {product_storage.qty}'
            )

        od = OrderDetail(product_sku=dto.sku, qty=dto.qty)
        order.order_details.append(od)

        product_storage.qty -= dto.qty
