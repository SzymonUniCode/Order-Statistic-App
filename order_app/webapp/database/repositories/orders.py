from sqlalchemy.orm import joinedload, selectinload

from webapp.extensions import db
from webapp.database.repositories.generic import GenericRepository
from webapp.database.models.orders import Order
from webapp.database.models.order_details import OrderDetail
from sqlalchemy import select


class TotalOrderRepository(GenericRepository[Order]):
    def __init__(self) -> None:
        super().__init__(Order)

    def get_all_total_orders(self) -> list[Order] | None:
        stmt = select(Order).join(Order.order_details)
        return list(db.session.scalars(stmt).all())

    def get_total_order(self, order_id: int) -> Order | None:
        stmt = select(Order).where(Order.id == order_id).join(Order.order_details)
        return db.session.scalar(stmt)


    def add_product_to_order(self, order: Order, product_sku: str, qty: int) -> OrderDetail | None:
        order_detail = OrderDetail(order_id=order.id, product_sku=product_sku, qty=qty)
        db.session.add(order_detail)
        return order_detail