from webapp.database.models.products import Product
from webapp.database.models.storage import Storage
from webapp.database.models.users import User
from webapp.database.models.orders import Order
from webapp.database.models.order_details import OrderDetail
from sqlalchemy.orm import Session


def test_product_model_repr_and_fields(session: Session, product: Product):
    product_from_db = session.get(Product, product.sku)
    assert product_from_db is not None

    assert product_from_db.sku == "SKU-123"
    assert product_from_db.name == "Product Test 1"
    assert product_from_db.price == 100.4

    rep = repr(product_from_db)
    assert "SKU='SKU-123'" in rep
    assert "name='Product Test 1'" in rep
    assert "100.4" in rep


def test_user_model_repr_and_fields(session: Session, user: User):
    user_from_db = session.get(User, user.id)
    assert user_from_db is not None

    assert user_from_db.username == "John Test"

    rep = repr(user_from_db)
    assert "username='John Test'" in rep


def test_storage_model_repr_and_fields(session: Session, storage: Storage):
    storage_from_db = session.get(Storage, storage.sku)
    assert storage_from_db is not None

    assert storage_from_db.sku == "SKU-123"
    assert storage_from_db.qty == 100

    rep = repr(storage_from_db)
    assert "sku='SKU-123'" in rep
    assert "qty=100" in rep


def test_order_model_and_fields(session: Session, order: Order):
    order_from_db = session.get(Order, order.id)
    assert order_from_db is not None

    assert order_from_db.id == 1
    assert order_from_db.user_id == 1

    rep = repr(order_from_db)
    assert f"User(id=1)"


def test_order_details_model_and_fields(session: Session, order_details_1: OrderDetail):
    order_details_from_db = session.get(OrderDetail, (order_details_1.order_id, order_details_1.product_sku))
    assert order_details_from_db is not None

    assert order_details_from_db.order_id == 1
    assert order_details_from_db.product_sku == "SKU-123"
    assert order_details_from_db.qty == 50

    rep = repr(order_details_from_db)
    assert f"<OrderDetail(order_id=1, product_sku=SKU-123, qty=50)>"