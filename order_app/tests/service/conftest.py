from unittest.mock import MagicMock
import pytest

from decimal import Decimal

from webapp.database.models.order_details import OrderDetail
from webapp.database.models.orders import Order
from webapp.database.models.products import Product
from webapp.database.models.storage import Storage
from webapp.database.models.users import User
from webapp.services.users.service import UserService
from webapp.services.storage.service import StorageService
from webapp.services.products.service import ProductService
from webapp.services.orders.service import OrderService


# -----------------------------------------------------------------------
# MOCK REPOSITORIES
# -----------------------------------------------------------------------

@pytest.fixture
def mock_order_repo():
    return MagicMock()

@pytest.fixture
def mock_storage_repo():
    return MagicMock()

@pytest.fixture
def mock_user_repo():
    return MagicMock()

@pytest.fixture
def mock_product_repo():
    return MagicMock()


# -----------------------------------------------------------------------
# MOCKED SERVICES
# -----------------------------------------------------------------------

@pytest.fixture
def mock_user_service(mock_user_repo):
    return UserService(mock_user_repo)


@pytest.fixture
def mock_storage_service(mock_storage_repo, mock_product_repo):
    return StorageService(mock_storage_repo, mock_product_repo)


@pytest.fixture
def mock_product_service(mock_product_repo):
    return ProductService(mock_product_repo)


@pytest.fixture
def mock_order_service(mock_order_repo, mock_storage_repo, mock_user_repo):
    return OrderService(
        order_repo=mock_order_repo,
        storage_repo=mock_storage_repo,
        user_repo=mock_user_repo
    )


@pytest.fixture
def fake_user_with_orders():
    user = User(username="John Test 1")
    user.id = 1
    user.orders = [MagicMock(), MagicMock(), MagicMock()]
    return user


@pytest.fixture
def fake_products():
    return [
        Product(sku="SKU-1", name="Test Product 1", price=Decimal(10.0)),
        Product(sku="SKU-2", name="Test Product 2", price=Decimal(20.0)),
        Product(sku="SKU-3", name="Test Product 3", price=Decimal(30.0))
    ]


@pytest.fixture
def fake_storage():
    return [
        Storage(sku="SKU-1", qty=10),
        Storage(sku="SKU-2", qty=20),
        Storage(sku="SKU-3", qty=30)
    ]

@pytest.fixture
def fake_order_details_1():
    return [
        OrderDetail(order_id=1, product_sku="SKU-1", qty=10),
        OrderDetail(order_id=1, product_sku="SKU-2", qty=20),
        OrderDetail(order_id=1, product_sku="SKU-3", qty=30)
    ]


@pytest.fixture
def fake_order_details_2():
    return [
        OrderDetail(order_id=2, product_sku="SKU-2", qty=20),
        OrderDetail(order_id=2, product_sku="SKU-3", qty=30),
        OrderDetail(order_id=2, product_sku="SKU-4", qty=40)
    ]


@pytest.fixture
def fake_orders_with_details(fake_order_details_1, fake_order_details_2, fake_user_with_orders):
    o1 = Order(id=1, user_id=1, order_details=fake_order_details_1)
    o1.user = fake_user_with_orders

    o2 = Order(id=2, user_id=1, order_details=fake_order_details_2)
    o2.user = fake_user_with_orders

    return [o1, o2]