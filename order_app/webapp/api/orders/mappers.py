from webapp.api.orders.schemas import (
    OrderResponseSchema,
    OrderDetailsResponseSchema,
    CreateOrderDetailSchema,
    CreateOrderSchema,
    DeleteProductInOrderSchema
)

from webapp.services.orders.dtos import ReadOrderDTO, CreateOrderDTO, CreateOrderDetailDTO, ReadOrderDetailDTO, \
    DeleteProductsInOrderDTO


def to_schema_order_details_response(dto: ReadOrderDetailDTO) -> OrderDetailsResponseSchema:
    return OrderDetailsResponseSchema(
        sku=dto.sku,
        qty=dto.qty
    )

def to_schema_orders_response(dto: ReadOrderDTO) -> OrderResponseSchema:
    return OrderResponseSchema(
        id=dto.id,
        user_name=dto.user_name,
        details=[to_schema_order_details_response(detail) for detail in dto.details]
    )


def to_dto_create_order_detail(schema: CreateOrderDetailSchema) -> CreateOrderDetailDTO:
    return CreateOrderDetailDTO(
        sku=schema.sku,
        qty=schema.qty
    )


def to_dto_create_order(schema: CreateOrderSchema) -> CreateOrderDTO:
    return CreateOrderDTO(
        user_name=schema.user_name,
        details=[to_dto_create_order_detail(detail) for detail in schema.details]
    )


def to_dto_delete_product_in_order(schema: DeleteProductInOrderSchema) -> DeleteProductsInOrderDTO:
    return DeleteProductsInOrderDTO(
        order_id=schema.order_id,
        product_sku=schema.product_sku
    )