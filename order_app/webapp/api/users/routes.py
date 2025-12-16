from flask import request, jsonify
from flask.typing import ResponseReturnValue
from dependency_injector.wiring import inject, Provide
from webapp.api.users.schemas import CreateUserSchema
from webapp.api.users.mappers import to_schemas_user_response, to_dto_create_user

from webapp.services.users.service import UserService
from webapp.container import Container
from . import user_bp

@user_bp.get("/")
@inject
def get_all(user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    read_dto = user_service.get_all()
    return jsonify([to_schemas_user_response(user).model_dump(mode='json') for user in read_dto]), 200


@user_bp.get("/<username>")
@inject
def get_by_username(username: str, user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    user_dto = user_service.get_by_username(username)
    return jsonify(to_schemas_user_response(user_dto).model_dump(mode='json')), 200


@user_bp.delete("/<int:user_id>")
@inject
def delete_user_by_id(user_id: int, user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    result = user_service.delete_user_by_id(user_id)
    return jsonify({"message": result}), 200

@user_bp.post("/")
@inject
def create_user(user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    payload = CreateUserSchema.model_validate(request.get_json or {})
    dto = to_dto_create_user(payload)
    read_dto = user_service.add_user(dto)
    return jsonify(to_schemas_user_response(read_dto).model_dump(mode='json')), 201
