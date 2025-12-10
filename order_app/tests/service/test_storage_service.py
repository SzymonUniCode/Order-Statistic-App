from decimal import Decimal
from unittest.mock import patch, MagicMock
import pytest

from webapp.database.models.products import Product
from webapp.database.models.storage import Storage
from webapp.database.repositories.storage import StorageRepository
from webapp.services.storage.service import StorageService
from webapp.services.exceptions import NotFoundException, ProductAlreadyExistsException
from webapp.services.storage.dtos import ModifyStorageDTO



def test_get_all(mock_storage_service, mock_storage_repo, fake_storage):

    mock_storage_repo.get_all.return_value = fake_storage

    result = mock_storage_service.get_all()

    assert len(result) == 3

    assert result[0].sku == "SKU-1"
    assert result[0].quantity == 10

    assert result[2].sku == "SKU-3"
    assert result[2].quantity == 30


def test_get_by_sku(mock_storage_service, mock_storage_repo, fake_storage):

    mock_storage_repo.get_by_sku.return_value = fake_storage[0]

    result = mock_storage_service.get_by_sku("SKU-1")

    assert result.sku == "SKU-1"
    assert result.quantity == 10


@pytest.mark.parametrize(
    'min_qty, max_qty, expected_sku, expected_len',
    [
        (10, 100, ["SKU-1", "SKU-2", "SKU-3"], 3),
        (11, 100, ["SKU-2", "SKU-3"], 2),
        (22, 30, ["SKU-3"], 1)
    ]
)
def test_get_by_qty_between(
        mock_storage_service,
        mock_storage_repo,
        fake_storage,
        min_qty: int,
        max_qty: int,
        expected_sku: list[str],
        expected_len: int
    ):


    filtered = [fs for fs in fake_storage if min_qty <= fs.qty <= max_qty]

    mock_storage_repo.get_by_qty_between.return_value = filtered

    result = mock_storage_service.get_by_qty_between(min_qty, max_qty)

    assert len(result) == expected_len
    assert all(r.sku in expected_sku for r in result)



@patch("webapp.services.storage.service.db")
def test_add_product_to_storage_success(mock_db, mock_storage_service, mock_storage_repo, mock_product_repo, fake_storage):

    mock_db.sesscion.begin.return_value.__enter__.return_value = None


    dto = ModifyStorageDTO(sku="SKU-4", quantity=40)

    mock_product_repo.get_by_sku.return_value = MagicMock()
    mock_storage_repo.get_by_sku.return_value = None

    result = mock_storage_service.add_product_to_storage(dto)


    mock_storage_repo.add.assert_called_once()
    assert "Product SKU-4 added to storage with qty 40"


@patch("webapp.services.storage.service.db")
def test_add_product_to_storage_error_in_products(
        mock_db,
        mock_storage_service,
        mock_product_repo,
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    mock_product_repo.get_by_sku.return_value = None

    with pytest.raises(NotFoundException):
        mock_storage_service.add_product_to_storage(ModifyStorageDTO(sku="SKU-4", quantity=40))



@patch("webapp.services.storage.service.db")
def test_add_product_to_storage_error_in_storage(
        mock_db,
        mock_storage_service,
        mock_storage_repo,
        mock_product_repo,
    ):

    mock_db.session.begin.return_value.__enter__.return_value = None

    mock_product_repo.get_by_sku.return_value = MagicMock()
    mock_storage_repo.get_by_sku.return_value = MagicMock()

    with pytest.raises(ProductAlreadyExistsException):
        mock_storage_service.add_product_to_storage(ModifyStorageDTO(sku="SKU-4", quantity=40))


@patch("webapp.services.storage.service.db")
def test_add_qty_to_storage_sku_success(mock_db, mock_storage_service, mock_storage_repo, mock_product_repo, fake_storage):

    mock_db.session.begin.return_value.__enter__.return_value = None

    dto = ModifyStorageDTO(sku="SKU-1", quantity=10)

    mock_product_repo.get_by_sku.return_value = MagicMock()
    mock_storage_repo.get_by_sku.return_value = fake_storage[0]

    result_1 = mock_storage_service.add_qty_to_storage_sku(dto)

    assert result_1 == "10 added to SKU-1"
    assert fake_storage[0].qty == 20
