from flask import Flask, jsonify
from flask.typing import ResponseReturnValue
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from webapp.services.exceptions import ServiceException


def register_error_handlers(app: Flask) -> None:

    # -------------------------------
    # Pydantic validation (400)
    # -------------------------------
    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_error(error: ValidationError) -> ResponseReturnValue:
        return jsonify({
            "error": "Validation error",
            "details": error.errors(),
        }), 400

    # -------------------------------
    # Domain / Service exceptions
    # -------------------------------
    @app.errorhandler(ServiceException)
    def handle_service_exception(error: ServiceException) -> ResponseReturnValue:
        return jsonify({
            "error": str(error),
        }), error.status_code

    # -------------------------------
    # HTTP errors (404, 405, etc.)
    # -------------------------------
    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException) -> ResponseReturnValue:
        return jsonify({
            "error": error.name,
            "description": error.description,
        }), error.code

    # -------------------------------
    # REAL fallback (500)
    # -------------------------------
    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception) -> ResponseReturnValue:
        app.logger.exception("Unhandled exception")
        return jsonify({
            "error": "Internal server error"
        }), 500