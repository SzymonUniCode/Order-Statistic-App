from unittest.mock import patch, MagicMock
import pytest

from webapp.database.models.orders import Order
from webapp.database.models.order_details import OrderDetail
from webapp.database.models.storage import Storage
from webapp.database.models.users import User
from webapp.database.repositories.orders import TotalOrderRepository
from webapp.database.repositories.products import ProductRepository
from webapp.database.repositories.users import UserRepository
from webapp.services.orders.mappers import read_dto_order_details_to_order_details

from webapp.services.orders.service import OrderService
from webapp.services.exceptions import NotFoundException, ProductAlreadyExistsException, NotEnoughStockException, \
    ServiceException
from webapp.services.orders.dtos import CreateOrderDTO, ReadOrderDTO, CreateOrderDetailDTO, DeleteProductsInOrderDTO


def test_get_all_orders_with_details(mock_order_service, mock_order_repo, fake_orders_with_details):

    mock_order_repo.get_all_total_orders.return_value = fake_orders_with_details

    result = mock_order_service.get_all_orders_with_details()

    assert len(result) == 2
    assert len(result[0].details) == 3



def test_mapper_read_dto_order_details_to_order_details():
    dto = CreateOrderDetailDTO(sku="SKU-1", qty=10)

    result = read_dto_order_details_to_order_details(dto)

    assert isinstance(result, OrderDetail)
    assert result.product_sku == "SKU-1"
    assert result.qty == 10


def test_get_order_with_details_by_id_success(mock_order_service, mock_order_repo, fake_orders_with_details):

    mock_order_repo.get_total_order_by_id.return_value = fake_orders_with_details[0]

    result = mock_order_service.get_order_with_details_by_id(1)

    assert result is not None
    assert result.id == 1
    assert result.user_name == "John Test 1"
    assert len(result.details) == 3


def test_get_order_with_details_by_id_error(mock_order_service, mock_order_repo, fake_orders_with_details):

    mock_order_repo.get_total_order_by_id.return_value = None

    with pytest.raises(NotFoundException):
        mock_order_service.get_order_with_details_by_id(1)





def test_get_all_orders_by_user_name_success(mock_order_service, mock_order_repo, mock_user_repo, fake_orders_with_details):

    mock_user_repo.get_by_username.return_value = MagicMock()

    mock_order_repo.get_total_orders_by_user_name.return_value = fake_orders_with_details

    result = mock_order_service.get_all_orders_by_user_name("John Test 1")



    mock_user_repo.get_by_username.assert_called_once_with("John Test 1")
    mock_order_repo.get_total_orders_by_user_name.assert_called_once_with("John Test 1")

    assert len(result) == 2
    assert result[0].user_name == "John Test 1"
    assert result[1].user_name == "John Test 1"
    assert len(result[0].details) == 3
    assert len(result[1].details) == 3



def test_get_all_orders_by_user_name_error(mock_order_service, mock_order_repo, mock_user_repo, fake_orders_with_details):

    mock_user_repo.get_by_username.return_value = None

    with pytest.raises(NotFoundException):
        mock_order_service.get_all_orders_by_user_name("John Test 1")

    mock_user_repo.get_by_username.assert_called_once_with("John Test 1")




@patch("webapp.services.orders.service.db")
def test_add_order_with_details_success(
        mock_db,
        mock_order_service,
        mock_order_repo,
        mock_user_repo,
        mock_storage_repo
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    dto_details = CreateOrderDetailDTO("SKU-1", qty=10)
    dto = CreateOrderDTO(user_name="John Test 1", details=[dto_details])

    # Mock User
    user_obj = User(id=1, username="John Test 1")
    mock_user_repo.get_by_username.return_value = user_obj

    # Mock Order Created in DB
    order_obj = Order(user_id=1)
    order_obj.id = 1                                # flush() simulation to get id in DB
    order_obj.order_details = []                    # also with a flush() we have full object of Order so empty list as well
    mock_order_repo.add.return_value = order_obj

    # Mock Storage
    storage_obj = Storage(sku="SKU-1", qty=100)
    mock_storage_repo.get_by_sku_for_update.return_value = storage_obj     # if None gives error


    result = mock_order_service.add_order_with_details(dto)


    # ASSERTS

    mock_user_repo.get_by_username.assert_called_once_with("John Test 1")
    mock_order_repo.add.assert_called_once()
    mock_storage_repo.get_by_sku_for_update.assert_called_once_with("SKU-1")

    assert result == "Order 1 created successfully with 1 products"

    assert storage_obj.qty == 90

    assert len(order_obj.order_details) == 1
    assert order_obj.order_details[0].product_sku == "SKU-1"
    assert order_obj.order_details[0].qty == 10



@patch("webapp.services.orders.service.db")
def test_add_order_with_details_error_no_user(
        mock_db,
        mock_order_service,
        mock_order_repo,
        mock_user_repo,
        mock_storage_repo
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    dto_details = CreateOrderDetailDTO("SKU-1", qty=10)
    dto = CreateOrderDTO(user_name="John Test 1", details=[dto_details])

    mock_user_repo.get_by_username.return_value = None

    with pytest.raises(NotFoundException):
        mock_order_service.add_order_with_details(dto)

    mock_user_repo.get_by_username.assert_called_once_with("John Test 1")




@pytest.mark.parametrize(
    "test_qty",
    [0, -1, -254]

)
@patch("webapp.services.orders.service.db")
def test_add_order_with_details_error_wrong_qty(
        mock_db,
        mock_order_service,
        mock_order_repo,
        mock_user_repo,
        mock_storage_repo,
        test_qty: int
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    dto_details = CreateOrderDetailDTO("SKU-1", qty=test_qty)
    dto = CreateOrderDTO(user_name="John Test 1", details=[dto_details])

    with pytest.raises(ServiceException):
        mock_order_service.add_order_with_details(dto)




@patch("webapp.services.orders.service.db")
def test_add_order_with_details_error_no_sku(
        mock_db,
        mock_order_service,
        mock_order_repo,
        mock_user_repo,
        mock_storage_repo
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    dto_details = CreateOrderDetailDTO("", qty=10)
    dto = CreateOrderDTO(user_name="John Test 1", details=[dto_details])

    with pytest.raises(ServiceException):
        mock_order_service.add_order_with_details(dto)




@patch("webapp.services.orders.service.db")
def test_add_product_to_order_success(
        mock_db,
        mock_order_service,
        mock_order_repo,
        mock_storage_repo,
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    dto_details = CreateOrderDetailDTO("SKU-2", qty=10)
    order_obj = Order(id=1, user_id=1, order_details = [OrderDetail(product_sku="SKU-1", qty=10)])

    mock_order_repo.get.return_value = order_obj

    storage_obj = Storage(sku="SKU-2", qty=100)
    mock_storage_repo.get_by_sku_for_update.return_value = storage_obj

    result = mock_order_service.add_product_to_order(1, dto_details)

    assert result == "Product SKU-2 of 10 qty added to order 1 successfully"
    assert storage_obj.qty == 90



@patch("webapp.services.orders.service.db")
def test_add_product_to_order_error_no_order(
        mock_db,
        mock_order_service,
        mock_order_repo,
        mock_storage_repo,
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    dto_details = CreateOrderDetailDTO("SKU-2", qty=10)

    mock_order_repo.get.return_value = None


    with pytest.raises(ServiceException):
        mock_order_service.add_product_to_order(1, dto_details)

    mock_order_repo.get.assert_called_once_with(1)



@patch("webapp.services.orders.service.db")
def test_add_product_to_order_error_product_already_exists_in_order(
        mock_db,
        mock_order_service,
        mock_order_repo,
        mock_storage_repo,
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    dto_details = CreateOrderDetailDTO("SKU-1", qty=10)
    order_obj = Order(id=1, user_id=1, order_details = [OrderDetail(product_sku="SKU-1", qty=10)])

    mock_order_repo.get.return_value = order_obj

    with pytest.raises(ProductAlreadyExistsException):
        mock_order_service.add_product_to_order(1, dto_details)

    mock_order_repo.get.assert_called_once_with(1)


@patch("webapp.services.orders.service.db")
def test_add_product_to_order_error_no_product_in_storage(
        mock_db,
        mock_order_service,
        mock_order_repo,
        mock_storage_repo,
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    dto_details = CreateOrderDetailDTO("SKU-2", qty=10)
    order_obj = Order(id=1, user_id=1, order_details = [OrderDetail(product_sku="SKU-1", qty=10)])

    mock_order_repo.get.return_value = order_obj

    mock_storage_repo.get_by_sku_for_update.return_value = None

    with pytest.raises(NotFoundException):
        mock_order_service.add_product_to_order(1, dto_details)

    mock_order_repo.get.assert_called_once_with(1)



@patch("webapp.services.orders.service.db")
def test_add_product_to_order_error_not_enough_qty_in_storage(
        mock_db,
        mock_order_service,
        mock_order_repo,
        mock_storage_repo,
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    dto_details = CreateOrderDetailDTO("SKU-2", qty=10)
    order_obj = Order(id=1, user_id=1, order_details = [OrderDetail(product_sku="SKU-1", qty=10)])

    mock_order_repo.get.return_value = order_obj

    storage_obj = Storage(sku="SKU-2", qty=1)
    mock_storage_repo.get_by_sku_for_update.return_value = storage_obj

    with pytest.raises(NotEnoughStockException):
        mock_order_service.add_product_to_order(1, dto_details)

    mock_order_repo.get.assert_called_once_with(1)




@patch("webapp.services.orders.service.db")
def test_delete_order_with_details_success(
        mock_db,
        mock_order_service,
        mock_order_repo,
        mock_storage_repo
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    order_obj = Order(id=1, user_id=1, order_details=[OrderDetail(product_sku="SKU-1", qty=10)])

    result = mock_order_service.delete_order_with_details(order_obj.id)

    assert result == "Order 1 deleted with all details"



@patch("webapp.services.orders.service.db")
def test_delete_product_in_order_success(
        mock_db,
        mock_order_service,
        mock_order_repo,
        mock_storage_repo,
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    dto = DeleteProductsInOrderDTO(order_id=1, product_sku="SKU-1")

    order_obj = Order(id=1, user_id=1, order_details=[
        OrderDetail(product_sku="SKU-1", qty=10),
        OrderDetail(product_sku="SKU-2", qty=10)
    ])

    mock_order_repo.get.return_value = order_obj

    storage_obj = Storage(sku="SKU-1", qty=190)
    mock_storage_repo.get_by_sku_for_update.return_value = storage_obj

    result = mock_order_service.delete_product_in_order(dto)

    assert result == 'Product SKU-1 deleted from order 1'
    assert len(order_obj.order_details) == 1
    assert order_obj.order_details[0].product_sku == "SKU-2"
    assert storage_obj.qty == 200



@patch("webapp.services.orders.service.db")
def test_delete_product_in_order_error_no_order(
        mock_db,
        mock_order_service,
        mock_order_repo,
        mock_storage_repo,
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    dto = DeleteProductsInOrderDTO(order_id=1, product_sku="SKU-1")

    mock_order_repo.get.return_value = None

    with pytest.raises(NotFoundException):
        mock_order_service.delete_product_in_order(dto)

    mock_order_repo.get.assert_called_once_with(1)



@patch("webapp.services.orders.service.db")
def test_delete_product_in_order_error_no_product_in_order(
        mock_db,
        mock_order_service,
        mock_order_repo,
        mock_storage_repo,
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    dto = DeleteProductsInOrderDTO(order_id=1, product_sku="SKU-3")

    order_obj = Order(id=1, user_id=1, order_details=[
        OrderDetail(product_sku="SKU-1", qty=10),
        OrderDetail(product_sku="SKU-2", qty=10)
    ])

    mock_order_repo.get.return_value = order_obj

    with pytest.raises(NotFoundException):
        mock_order_service.delete_product_in_order(dto)

    mock_order_repo.get.assert_called_once_with(1)




@patch("webapp.services.orders.service.db")
def test_delete_product_in_order_error_no_product_in_storage(
        mock_db,
        mock_order_service,
        mock_order_repo,
        mock_storage_repo,
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    dto = DeleteProductsInOrderDTO(order_id=1, product_sku="SKU-1")

    order_obj = Order(id=1, user_id=1, order_details=[
        OrderDetail(product_sku="SKU-1", qty=10),
        OrderDetail(product_sku="SKU-2", qty=10)
    ])

    mock_order_repo.get.return_value = order_obj

    mock_storage_repo.get_by_sku_for_update.return_value = None

    with pytest.raises(NotFoundException):
        mock_order_service.delete_product_in_order(dto)

    mock_order_repo.get.assert_called_once_with(1)
    mock_storage_repo.get_by_sku_for_update.assert_called_once_with("SKU-1")