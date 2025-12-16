from flask import request, jsonify
from flask.typing import ResponseReturnValue
from dependency_injector.wiring import inject, Provide
from webapp.api.products.schemas import CreateProductSchema
from webapp.api.products.mappers import to_schemas_product_response, to_dto_create_product
from decimal import Decimal

from webapp.services.products.service import ProductService
from webapp.container import Container
from . import product_bp


@product_bp.get("/")
@inject
def get_all(product_service: ProductService = Provide[Container.product_service]) -> ResponseReturnValue:
    products = product_service.get_all()
    return jsonify([to_schemas_product_response(product).model_dump(mode="json") for product in products]), 200

@product_bp.get("/sku/<string:sku>")
@inject
def get_by_sku(sku: str, product_service: ProductService = Provide[Container.product_service]) -> ResponseReturnValue:
    product = product_service.get_by_sku(sku)
    return jsonify(to_schemas_product_response(product).model_dump(mode="json")), 200


@product_bp.get("/price")
@inject
def get_by_price_between(
        product_service: ProductService = Provide[Container.product_service]
    ) -> ResponseReturnValue:

    price_min = request.args.get("min", default=Decimal("0"), type=Decimal)
    price_max = request.args.get("max",default=Decimal("9999999999"), type=Decimal)

    products = product_service.get_by_price_between(price_min, price_max)
    return jsonify([to_schemas_product_response(product).model_dump(mode="json") for product in products]), 200


@product_bp.post("/")
@inject
def create_product(product_service: ProductService = Provide[Container.product_service]) -> ResponseReturnValue:
    payload = CreateProductSchema.model_validate(request.get_json() or {})
    read_dto = to_dto_create_product(payload)
    dto = product_service.create_product(read_dto)
    return jsonify(to_schemas_product_response(dto).model_dump(mode="json")), 201