from webapp.database.models.orders import Order
from webapp.database.models.order_details import OrderDetail

from webapp.services.orders.dtos import ReadOrderDTO, ReadOrderDetailDTO, CreateOrderDTO, CreateOrderDetailDTO



def order_to_dto(order: Order) -> ReadOrderDTO:
    return ReadOrderDTO(
        id=order.id,
        user_name=order.user.username if order.user else "",
        details=[order_detail_to_dto(od) for od in order.order_details]
    )


def order_detail_to_dto(order_detail: OrderDetail) -> ReadOrderDetailDTO:
    return ReadOrderDetailDTO(
        sku = order_detail.product_sku,
        qty = order_detail.qty,
    )


def read_dto_order_details_to_order_details(order_detail: CreateOrderDetailDTO) -> OrderDetail:
    return OrderDetail(
        product_sku = order_detail.sku,
        qty = order_detail.qty,
    )