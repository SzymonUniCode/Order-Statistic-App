from flask.testing import FlaskClient



def test_get_all_users(client: FlaskClient, seed_user_data) -> None:
    resp = client.get("/api/users/")
    assert resp.status_code == 200

    data = resp.get_json()
    assert len(data) == 2
    assert {u["name"] for u in data} == {"John Test 1", "John Test 2"}


def test_get_by_username(client: FlaskClient, seed_user_data) -> None:
    resp = client.get("/api/users/John Test 1")

    assert resp.status_code == 200
    assert resp.get_json()["name"] == "John Test 1"


def test_delete_user_by_id(client: FlaskClient, seed_user_data) -> None:
    users = client.get("/api/users/").get_json()
    user_id = next(u["id"] for u in users if u["name"] == "John Test 1")

    resp = client.delete(f"/api/users/{user_id}")
    assert resp.status_code == 200

    remaining = client.get("/api/users/").get_json()
    assert len(remaining) == 1
    assert remaining[0]["name"] == "John Test 2"


def test_create_user(client: FlaskClient, seed_user_data) -> None:
    resp = client.post("/api/users/", json={"name": "Test User 3"})
    assert resp.status_code == 201

    users = client.get("/api/users/").get_json()
    assert len(users) == 3
    assert users[-1]["name"] == "Test User 3"

