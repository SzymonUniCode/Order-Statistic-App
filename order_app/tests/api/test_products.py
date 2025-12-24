from decimal import Decimal

from flask.testing import FlaskClient



def test_get_all_products(client: FlaskClient, seed_product_data) -> None:
    resp = client.get("/api/products/")
    assert resp.status_code == 200

    data = resp.get_json()
    assert len(data) == 2
    assert {u["sku"] for u in data} == {"SKU-1", "SKU-2"}


def test_get_by_sku(client: FlaskClient, seed_product_data) -> None:
    resp = client.get("/api/products/sku/SKU-1")

    assert resp.status_code == 200
    assert resp.get_json()["name"] == "Test 1"


def test_get_by_price_between(client: FlaskClient, seed_product_data) -> None:
    resp = client.get("/api/products/price?min=9&max=12")

    assert resp.status_code == 200

    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["sku"] == "SKU-1"
    assert data[0]["price"] == "10.00"