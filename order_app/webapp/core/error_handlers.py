from flask import Flask, jsonify
from flask.typing import ResponseReturnValue
from pydantic import ValidationError

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
    # Fallback (500)
    # -------------------------------
    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception) -> ResponseReturnValue:
        app.logger.exception("Unhandled exception")
        return jsonify({
            "error": "Internal server error"
        }), 500