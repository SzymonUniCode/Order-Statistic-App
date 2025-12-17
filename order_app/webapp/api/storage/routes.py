from flask import jsonify, request
from flask.typing import ResponseReturnValue
from dependency_injector.wiring import inject, Provide

from webapp.api.storage.schemas import StorageResponseSchema, ModifyStorageSchema
from webapp.api.storage.mappers import to_schema_storage_response, to_dto_modify_storage


from webapp.services.storage.service import StorageService
from webapp.container import Container
from . import storage_bp


@storage_bp.get("/")
@inject
def get_all(storage_service: StorageService = Provide[Container.storage_service]):
    storages = storage_service.get_all()
    return jsonify([to_schema_storage_response(storage).model_dump(mode="json") for storage in storages]), 200


@storage_bp.get("/sku/<string:sku>")
@inject
def get_by_sku(sku: str, storage_service: StorageService = Provide[Container.storage_service]):
    storage = storage_service.get_by_sku(sku)
    return jsonify(to_schema_storage_response(storage).model_dump(mode="json")), 200


@storage_bp.get("/qty")
@inject
def get_by_price_between(storage_service: StorageService = Provide[Container.storage_service]):

    min_qty = request.args.get("min", default=0, type=int)
    max_qty = request.args.get("max",default=9999999999, type=int)

    storages = storage_service.get_by_qty_between(min_qty, max_qty)

    return jsonify([to_schema_storage_response(storage).model_dump(mode="json") for storage in storages]), 200


@storage_bp.post("/")
@inject
def add_product_to_storage(storage_service: StorageService = Provide[Container.storage_service]) -> ResponseReturnValue:
    payload = ModifyStorageSchema.model_validate(request.get_json() or {})
    dto = to_dto_modify_storage(payload)
    result = storage_service.add_product_to_storage(dto)
    return jsonify({"message": result}), 201


# in the future possible implement better way without this schemas -> /<sku>/add and schemas validate only qty
@storage_bp.patch("/add")
@inject
def add_qty_to_storage_sku(storage_service: StorageService = Provide[Container.storage_service]) -> ResponseReturnValue:
    payload = ModifyStorageSchema.model_validate(request.get_json() or {})
    dto = to_dto_modify_storage(payload)
    result = storage_service.add_qty_to_storage_sku(dto)
    return jsonify({"message": result}), 200


@storage_bp.patch("/deduct")
@inject
def deduct_qty_from_storage_sku(storage_service: StorageService = Provide[Container.storage_service]) -> ResponseReturnValue:
    payload = ModifyStorageSchema.model_validate(request.get_json() or {})
    dto = to_dto_modify_storage(payload)
    result = storage_service.deduct_qty_from_storage_sku(dto)
    return jsonify({"message": result}), 200


@storage_bp.delete("/remove/<string:sku>")
@inject
def delete_product_from_storage(
        sku: str,
        storage_service: StorageService = Provide[Container.storage_service]
    ) -> ResponseReturnValue:
    result = storage_service.delete_storage_sku(sku)
    return jsonify({"message": result}), 200


