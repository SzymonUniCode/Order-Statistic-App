from decimal import Decimal
from unittest.mock import patch, MagicMock
import pytest

from webapp.database.models.products import Product
from webapp.database.repositories.products import ProductRepository
from webapp.services.products.service import ProductService
from webapp.services.exceptions import NotFoundException, ProductAlreadyExistsException
from webapp.services.products.dtos import CreateProductDTO



def test_get_all(
        mock_product_service: ProductService,
        mock_product_repo: MagicMock,
        fake_products: list[Product]
    ):

    mock_product_repo.get_all.return_value = fake_products

    result = mock_product_service.get_all()

    assert result is not None
    assert len(result) == 3

    assert result[0].sku == "SKU-1"
    assert result[0].name == "Test Product 1"
    assert result[0].price == 10.0

    assert result[1].sku == "SKU-2"
    assert result[1].name == "Test Product 2"
    assert result[1].price == 20.0

    assert result[2].sku == "SKU-3"
    assert result[2].name == "Test Product 3"
    assert result[2].price == 30.0



def test_get_by_sku_success(
        mock_product_service: ProductService,
        mock_product_repo: MagicMock,
        fake_products: list[Product],
        sku = "SKU-3"
    ):

    mock_product_repo.get_by_sku.return_value = fake_products[2]

    result = mock_product_service.get_by_sku(sku)

    assert result is not None
    assert result.sku == "SKU-3"



def test_get_by_sku_error(
        mock_product_service: ProductService,
        mock_product_repo: MagicMock,

    ):

    mock_product_repo.get_by_sku.return_value = None

    with pytest.raises(NotFoundException):
        mock_product_service.get_by_sku("SKU-4")





@pytest.mark.parametrize(
    "min_price, max_price, expected_sku, expected_len",
     [
        (Decimal(10), Decimal(100.9), ["SKU-1", "SKU-2", "SKU-3"], 3),
        (Decimal(10.1), Decimal(10000.9), ["SKU-2", "SKU-3"], 2),
        (Decimal(20), Decimal(30), ["SKU-2", "SKU-3"], 2),
        (Decimal(20.1), Decimal(30), ["SKU-3"], 1),
     ]
)
def test_get_by_price_between_success(
        mock_product_service: ProductService,
        mock_product_repo: MagicMock,
        fake_products: list[Product],
        min_price: Decimal,
        max_price: Decimal,
        expected_sku: list[str],
        expected_len: int
    ):

    filtered = [p for p in fake_products if min_price <= p.price <= max_price]
    mock_product_repo.get_by_price_between.return_value = filtered

    result = mock_product_service.get_by_price_between(min_price, max_price)

    assert result is not None
    assert len(result) == expected_len
    assert all(r.sku in expected_sku for r in result)


def test_get_by_price_between_error(
        mock_product_service: ProductService,
        mock_product_repo: MagicMock,

    ):

    mock_product_repo.get_by_price_between.return_value = []

    with pytest.raises(NotFoundException):
        mock_product_service.get_by_price_between(Decimal(100.0), Decimal(101.0))


def test_get_by_part_name_success(
        mock_product_service: ProductService,
        mock_product_repo: MagicMock,
        fake_products: list[Product],
        part_name: str = "Product"
    ):

    mock_product_repo.get_by_part_name.return_value = fake_products

    result = mock_product_service.get_by_part_name(part_name)

    assert result is not None
    assert len(result) == 3
    assert all(r.sku in ["SKU-1", "SKU-2", "SKU-3"] for r in result)


def test_get_by_part_name_error(
        mock_product_service: ProductService,
        mock_product_repo: MagicMock,

    ):

    mock_product_repo.get_by_part_name.return_value = []

    with pytest.raises(NotFoundException):
        mock_product_service.get_by_part_name("YOLO")



@patch("webapp.services.products.service.db")
def test_create_product_success(
        mock_db,
        mock_product_service,
        mock_product_repo
    ):
    mock_db.session.begin.return_value.__enter__.return_value = None

    dto = CreateProductDTO(sku="SKU-4", name="Test Product 4", price=Decimal(40.0))

    fake_product = Product(sku="SKU-4", name="Test Product 4", price=Decimal(40.0))

    mock_product_repo.get_by_sku.return_value = None

    mock_product_repo.add.return_value = fake_product

    result = mock_product_service.create_product(dto)

    mock_product_repo.add.assert_called_once()

    assert result.sku == "SKU-4"
    assert result.name == "Test Product 4"
    assert result.price == Decimal(40.0)


@patch("webapp.services.products.service.db")
def test_create_product_error(
        mock_db,
        mock_product_service: ProductService,
        mock_product_repo: MagicMock,
    ):
    mock_db.session.begin.return_value.__enter__.return_value = None

    mock_product_repo.get_by_sku.return_value = Product(
        sku="SKU-4", name="Test Product 4", price=Decimal(40.0)
    )

    with pytest.raises(ProductAlreadyExistsException):
        mock_product_service.create_product(
            CreateProductDTO(sku="SKU-4", name="Test Product 4", price=Decimal(40.0))
        )