from decimal import Decimal

import pytest
from flask.testing import FlaskClient
from werkzeug.exceptions import NotFound


def test_get_all_products(client: FlaskClient, seed_product_data) -> None:
    resp = client.get("/api/products/")
    assert resp.status_code == 200

    data = resp.get_json()
    assert len(data) == 2
    assert {u["sku"] for u in data} == {"SKU-1", "SKU-2"}


def test_get_by_sku(client: FlaskClient, seed_product_data) -> None:
    resp = client.get("/api/products/sku/SKU-1")

    assert resp.status_code == 200

    data = resp.get_json()
    assert data["name"] == "Test 1"
    assert data["sku"] == "SKU-1"


def test_get_by_price_between(client: FlaskClient, seed_product_data) -> None:
    resp = client.get("/api/products/price?min=9&max=12")

    assert resp.status_code == 200

    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["sku"] == "SKU-1"
    assert data[0]["price"] == "10.00"


def test_create_product(client: FlaskClient, seed_product_data) -> None:
    resp_1 = client.post("/api/products/", json={
        "sku": "SKU-3",
        "name": "Test 3",
        "price": "10.00",
    })

    assert resp_1.status_code == 201

    resp_2 = client.get("/api/products/")
    assert resp_2.status_code == 200

    data = resp_2.get_json()
    assert len(data) == 3
    assert any(p["sku"] == "SKU-3" for p in data)


def test_get_by_sku_not_found(client: FlaskClient, seed_product_data) -> None:
    resp = client.get("/api/products/sku/SKU-3")

    assert resp.status_code == 404

    data = resp.get_json()
    assert data["error"] == "Product with sku SKU-3 not found."