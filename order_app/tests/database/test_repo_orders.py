from webapp.database.models.orders import Order
from webapp.database.models.order_details import OrderDetail
from webapp.database.repositories.orders import TotalOrderRepository
from sqlalchemy.orm import Session
from webapp.database.models.products import Product


def test_add_order_and_get_all_total_orders(
        session: Session,
        order_repo: TotalOrderRepository,
        orders: list[Order],
        product_sku = "SKU-1",
        qty = 90
):

    order_repo.add_product_to_order(orders[2], product_sku, qty)

    orders_from_db = order_repo.get_all_total_orders()

    assert orders_from_db is not None
    assert len(orders_from_db) == 3

    assert orders_from_db[0].order_details[0].product_sku == "SKU-1"
    assert orders_from_db[0].order_details[0].qty == 10

    assert orders_from_db[0].order_details[1].product_sku == "SKU-2"
    assert orders_from_db[0].order_details[1].qty == 20

    assert orders_from_db[1].order_details[0].product_sku == "SKU-3"
    assert orders_from_db[1].order_details[0].qty == 30

    assert orders_from_db[2].order_details[0].product_sku == "SKU-1"
    assert orders_from_db[2].order_details[0].qty == 90



def test_get_total_order_by_id(session: Session, order_repo: TotalOrderRepository, orders: list[Order]):

    result = order_repo.get_total_order_by_id(order_id = 1)

    assert result is not None
    assert result.id == 1
    assert result.user_id == 1
    assert result.order_details is not None
    assert result.order_details[0].product_sku == "SKU-1"
    assert result.order_details[0].qty == 10
    assert result.order_details[1].product_sku == "SKU-2"
    assert result.order_details[1].qty == 20