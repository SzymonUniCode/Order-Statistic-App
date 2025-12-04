from webapp.database.models.products import Product
from webapp.services.products.dtos import ReadProductDTO
from decimal import Decimal

def product_to_dto(product: Product) -> ReadProductDTO:
    return ReadProductDTO(
        sku=str(product.sku),
        name=str(product.name),
        price=Decimal(product.price)
    )