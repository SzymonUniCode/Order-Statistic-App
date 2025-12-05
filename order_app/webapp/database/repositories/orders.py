from sqlalchemy.orm import joinedload, selectinload

from webapp.extensions import db
from webapp.database.repositories.generic import GenericRepository
from webapp.database.models.orders import Order
from webapp.database.models.order_details import OrderDetail
from webapp.database.models.products import Product

from sqlalchemy import select, desc


class TotalOrderRepository(GenericRepository[Order]):
    def __init__(self) -> None:
        super().__init__(Order)

    def get_all_total_orders(self) -> list[Order]:
        stmt = (
            select(Order)
            .options(
                joinedload(Order.order_details)
                .joinedload(OrderDetail.product)
            )
            .order_by(desc(Order.id))
        )

        result = db.session.execute(stmt).unique().scalars().all()
        return list(result)


    def get_total_order_by_id(self, order_id: int) -> Order | None:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                joinedload(Order.order_details)
                .joinedload(OrderDetail.product)
            )
        )

        return db.session.execute(stmt).unique().scalars().first()


    def get_total_orders_by_user_name(self, user_name: str) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.user.username == user_name)
            .options(
                joinedload(Order.order_details)
                .joinedload(OrderDetail.product)
            )
        )

        return db.session.execute(stmt).scalars().all()




    def add_product_to_order(self, order: Order, product_sku: str, qty: int) -> OrderDetail | None:
        order_detail = OrderDetail(
            order_id=order.id,
            product_sku=product_sku,
            qty=qty,
        )
        db.session.add(order_detail)

        return order_detail