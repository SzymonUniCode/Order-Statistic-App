from flask.testing import FlaskClient
import pytest

def test_get_all_orders(client: FlaskClient, seed_order_data) -> None:
    resp = client.get("/api/orders/")
    assert resp.status_code == 200

    data = resp.get_json()
    assert len(data) == 2

    data_by_id = {o["id"]: o for o in data}

    assert len(data_by_id[1]["details"]) == 2
    assert len(data_by_id[2]["details"]) == 1


def test_get_order_by_id(client: FlaskClient, seed_order_data) -> None:
    resp = client.get("/api/orders/order/1")
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["id"] == 1
    assert data["details"][0]["sku"] == "SKU-1"
    assert data["details"][1]["sku"] == "SKU-2"


def test_get_order_by_username(client: FlaskClient, seed_order_data) -> None:
    resp = client.get("/api/orders/user/John Test 2")
    assert resp.status_code == 200

    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["id"] == 2


def test_add_product_to_order(client: FlaskClient, seed_order_data, seed_storage_data, seed_product_data) -> None:
    resp_1 = client.post("/api/orders/2/items", json={"sku": "SKU-1", "qty": 1})
    assert resp_1.status_code == 201

    resp_2 = client.get("/api/orders/order/2")
    assert resp_2.status_code == 200
    data = resp_2.get_json()
    assert {sku["sku"] for sku in data["details"]} == {"SKU-3", "SKU-1"}



def test_add_order_with_details_and_delete_detail_in_order(client: FlaskClient, seed_order_data, seed_storage_data, seed_product_data) -> None:

    # Add order
    resp_1 = client.post(
        "/api/orders/add_order",
        json={
            "user_name": "John Test 1",
            "details": [
                {"sku": "SKU-1", "qty": 1}
            ]
        }
    )

    assert resp_1.status_code == 201

    # Check if the order was added
    resp_2 = client.get("api/orders/")
    assert resp_2.status_code == 200
    assert len(resp_2.get_json()) == 3

    # Check if the storage was updated
    resp_3 = client.get("/api/storage/sku/SKU-1")
    assert resp_3.status_code == 200
    assert resp_3.get_json()["quantity"] == 9

    # Delete product in order
    resp_4 = client.delete("/api/orders/delete_product", json = {"order_id": 1, "product_sku": "SKU-1"})
    assert resp_4.status_code == 200
    assert resp_4.get_json()["message"] == "Product SKU-1 deleted from order 1"

    # Check if the storage was updated
    resp_5 = client.get("/api/storage/")
    assert resp_5.status_code == 200
    data = resp_5.get_json()
    assert data[0]["quantity"] == 19


def test_delete_order_with_details(client: FlaskClient, seed_order_data) -> None:
    resp_1 = client.delete("/api/orders/1")
    assert resp_1.status_code == 200
    assert resp_1.get_json()["message"] == "Order 1 deleted with all details"

    resp_2 = client.get("/api/orders/")
    assert resp_2.status_code == 200
    assert len(resp_2.get_json()) == 1
