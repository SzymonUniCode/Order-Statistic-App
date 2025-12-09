from unittest.mock import MagicMock
import pytest

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
def mock_storage_service(mock_storage_repo):
    return StorageService(mock_storage_repo)


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