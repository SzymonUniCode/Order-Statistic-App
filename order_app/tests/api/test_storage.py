from flask.testing import FlaskClient
import pytest


def test_get_all_storage(client: FlaskClient, seed_storage_data) -> None:
    resp = client.get("/api/storage/")
    assert resp.status_code == 200

    data = resp.get_json()
    assert len(data) == 2
    assert {u["sku"] for u in data} == {"SKU-1", "SKU-2"}



def test_get_by_sku(client: FlaskClient, seed_storage_data) -> None:
    resp = client.get("/api/storage/sku/SKU-1")

    assert resp.status_code == 200

    data = resp.get_json()
    assert data["sku"] == "SKU-1"
    assert data["quantity"] == 10


def test_get_by_qty_between(client: FlaskClient, seed_storage_data) -> None:
    resp = client.get("/api/storage/qty?min=11&max=22")

    assert resp.status_code == 200

    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["sku"] == "SKU-2"
    assert data[0]["quantity"] == 20


def test_add_product_to_storage(client: FlaskClient, seed_storage_data, seed_product_data) -> None:
    resp_1 = client.post("/api/storage/", json={"sku": "SKU-4", "quantity": 40})

    assert resp_1.status_code == 201

    resp_2 = client.get("/api/storage/")
    assert resp_2.status_code == 200
    assert len(resp_2.get_json()) == 3
    assert {u["sku"] for u in resp_2.get_json()} == {"SKU-1", "SKU-2", "SKU-4"}


def test_add_qty_to_storage_sku(client: FlaskClient, seed_storage_data, seed_product_data) -> None:
    resp_1 = client.patch("/api/storage/add", json = {"sku": "SKU-1", "quantity": 101})

    assert resp_1.status_code == 200

    resp_2 = client.get("/api/storage/sku/SKU-1")
    assert resp_2.status_code == 200
    assert resp_2.get_json()["quantity"] == 111


def test_deduct_qty_from_storage_sku_and_deduct(client: FlaskClient, seed_storage_data, seed_product_data) -> None:
    resp_1 = client.patch("/api/storage/deduct", json = {"sku": "SKU-1", "quantity": 10})

    assert resp_1.status_code == 200

    resp_2 = client.get("/api/storage/sku/SKU-1")
    assert resp_2.status_code == 200
    assert resp_2.get_json()["quantity"] == 0

    resp_3 = client.delete("/api/storage/remove/SKU-1")

    assert resp_3.status_code == 200

    resp_4 = client.get("/api/storage/")
    assert resp_4.status_code == 200
    assert len(resp_4.get_json()) == 1
    assert {u["sku"] for u in resp_4.get_json()} == {"SKU-2"}

