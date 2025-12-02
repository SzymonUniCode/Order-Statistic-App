from webapp.database.models.products import Product
from webapp.database.repositories.products import ProductRepository
from sqlalchemy.orm import Session
from decimal import Decimal
import pytest


def test_get_by_part_name(session: Session, product_repo: ProductRepository, products: list[Product]):
    products_regular_text = product_repo.get_by_part_name("Test")
    products_small_text = product_repo.get_by_part_name("product")
    assert len(products_regular_text) == 3
    assert len(products_small_text) == 3


@pytest.mark.parametrize(
    "min_price, max_price, expected_sku, expected_len",
     [
        (Decimal(10), Decimal(100.9), ["SKU-1", "SKU-2"], 2),
        (Decimal(10), Decimal(10000.9), ["SKU-1", "SKU-2", "SKU-3"], 3),
        (Decimal(10.1), Decimal(100.8), ["SKU-1"], 1),
        (Decimal(100.9), Decimal(1000.4), ["SKU-2", "SKU-3"], 2),
     ]
)
def test_get_by_price(
        session: Session,
        product_repo: ProductRepository,
        products: list[Product],
        min_price:Decimal,
        max_price:Decimal,
        expected_sku:list[str],
        expected_len:int):

    result = product_repo.get_by_price_between(min_price, max_price)

    assert len(result) == expected_len

    result_skus = sorted([p.sku for p in result])   #typ: ignore
    assert result_skus == expected_sku


def test_get_by_sku(session: Session, product_repo: ProductRepository, products: list[Product]):
    products_sku = product_repo.get_by_sku("SKU-1")

    assert products_sku is not None
    assert products_sku.sku == "SKU-1"

