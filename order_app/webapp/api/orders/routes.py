from flask import jsonify, request
from flask.typing import ResponseReturnValue
from dependency_injector.wiring import inject, Provide

from webapp.api.orders.schemas import OrderResponseSchema, CreateOrderSchema, CreateOrderDetailSchema, \
    DeleteProductInOrderSchema
from webapp.api.orders.mappers import to_schema_orders_response, to_dto_create_order, to_dto_create_order_detail, \
    to_dto_delete_product_in_order

from webapp.services.orders.service import OrderService
from webapp.container import Container

from . import orders_bp


@orders_bp.get("/")
@inject
def get_all(order_service: OrderService = Provide[Container.order_service]) -> ResponseReturnValue:
    orders = order_service.get_all_orders_with_details()
    return jsonify([to_schema_orders_response(order).model_dump(mode="json") for order in orders]), 200



@orders_bp.get("/order/<int:order_id>")
@inject
def get_order_by_id(order_id: int, order_service: OrderService = Provide[Container.order_service]) -> ResponseReturnValue:
    order = order_service.get_order_with_details_by_id(order_id)
    return jsonify(to_schema_orders_response(order).model_dump(mode="json")), 200


@orders_bp.get("/user/<string:user_name>")
@inject
def get_orders_by_user_name(user_name: str, order_service: OrderService = Provide[Container.order_service]) -> ResponseReturnValue:
    orders = order_service.get_all_orders_by_user_name(user_name)
    return jsonify([to_schema_orders_response(order).model_dump(mode="json") for order in orders]), 200



@orders_bp.post("/add_order")
@inject
def add_order_with_details(order_service: OrderService = Provide[Container.order_service]):
    payload = CreateOrderSchema.model_validate(request.get_json() or {})
    dto = to_dto_create_order(payload)
    result = order_service.add_order_with_details(dto)
    return jsonify({"message":result}) , 200


@orders_bp.patch("/<int:order_id>/items")
@inject
def add_product_to_order(order_id: int, order_service: OrderService = Provide[Container.order_service]) -> ResponseReturnValue:
    payload = CreateOrderDetailSchema.model_validate(request.get_json() or {})
    dto = to_dto_create_order_detail(payload)
    result = order_service.add_product_to_order(order_id, dto)
    return jsonify({"message":result}), 200


@orders_bp.delete("/<int:order_id>")
@inject
def delete_order_with_details(
    order_id: int, order_service: OrderService = Provide[Container.order_service]) -> ResponseReturnValue:
    result = order_service.delete_order_with_details(order_id)
    return jsonify({"message": result}), 200


@orders_bp.delete("/delete_product")
@inject
def delete_product_in_order(
    order_service: OrderService = Provide[Container.order_service]
) -> ResponseReturnValue:
    payload = DeleteProductInOrderSchema.model_validate(request.get_json() or {})
    dto = to_dto_delete_product_in_order(payload)
    result = order_service.delete_product_in_order(dto)
    return jsonify({"message": result}), 200


# More REST API solution, where URL shows exactly whole operation. Schema is not needed in this solution.
# Schemas are way used mostly to create, update or partially modify(PATCH). In this case we delete.

# @orders_bp.delete("/<int:order_id>/items/<string:sku>")
# @inject
# def delete_product_in_order(
#     order_id: int,
#     sku: str,
#     order_service: OrderService = Provide[Container.order_service]
# ) -> ResponseReturnValue:
#     dto = DeleteProductsInOrderDTO(
#         order_id=order_id,
#         product_sku=sku
#     )
#     result = order_service.delete_product_in_order(dto)
#     return jsonify({"message": result}), 200