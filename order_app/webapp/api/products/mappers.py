from webapp.services.products.dtos import ReadProductDTO, CreateProductDTO
from webapp.api.products.schemas import ProductResponseSchema, CreateProductSchema


def to_schemas_product_response(dto: ReadProductDTO) -> ProductResponseSchema:
    return ProductResponseSchema(
        sku=dto.sku,
        name=dto.name,
        price=dto.price
    )


def to_dto_create_product(schema: CreateProductSchema) -> CreateProductDTO:
    return CreateProductDTO(
        sku=schema.sku,
        name=schema.name,
        price=schema.price
    )

