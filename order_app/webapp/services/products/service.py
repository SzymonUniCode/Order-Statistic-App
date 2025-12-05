from webapp.extensions import db

from webapp.database.models.products import Product

from webapp.database.repositories.products import ProductRepository

from webapp.services.exceptions import NotFoundException, ProductAlreadyExistsException

from webapp.services.products.dtos import CreateProductDTO, ReadProductDTO

from webapp.services.products.mappers import product_to_dto

from decimal import Decimal




class ProductService:

    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo


# ---------------------------------------------------------------------------------------
# Read methods
# ---------------------------------------------------------------------------------------
    def get_all(self) -> list[ReadProductDTO]:
        products = self.product_repo.get_all()
        return [product_to_dto(product) for product in products]


    def get_by_sku(self, sku: str) -> ReadProductDTO:
        product = self.product_repo.get_by_sku(sku)
        if product is None:
            raise NotFoundException(f"Product with sku {sku} not found.")
        return product_to_dto(product)


    def get_by_price_between(self, price_min: Decimal, price_max: Decimal) -> list[ReadProductDTO]:
        products = self.product_repo.get_by_price_between(price_min, price_max)
        if len(products) == 0:
            raise NotFoundException(f"Product with price between {price_min} and {price_max} not found.")
        return [product_to_dto(product) for product in products]


    def get_by_part_name(self, product_name: str) -> list[ReadProductDTO]:
        products = self.product_repo.get_by_part_name(product_name)
        if len(products) == 0:
            raise NotFoundException(f"Product with name {product_name} not found.")
        return [product_to_dto(product) for product in products]

# ---------------------------------------------------------------------------------------
# Create methods
# ---------------------------------------------------------------------------------------

    def create_product(self, dto: CreateProductDTO) -> ReadProductDTO:
        with db.session.begin():
            self._validate_product(dto.sku)
            product = Product(sku=dto.sku, name=dto.name, price=dto.price)
            self.product_repo.add(product)

        return product_to_dto(product)



# ---------------------------------------------------------------------------------------
# Privet methods
# ---------------------------------------------------------------------------------------
    def _validate_product(self, sku: str) -> Product | None:
        product = self.product_repo.get_by_sku(sku)

        if product is not None:
            raise ProductAlreadyExistsException(f"Product with sku {sku} already exists.")

        return None
