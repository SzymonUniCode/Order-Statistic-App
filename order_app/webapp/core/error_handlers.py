from flask import Flask, jsonify
from flask.typing import ResponseReturnValue


def register_error_handlers(app: Flask) -> None:

    # -------------------------------
    # 404 - Not Found
    # -------------------------------
    @app.errorhandler(404)
    def handle_not_found_error(error: Exception) -> ResponseReturnValue:
        app.logger.warning(f"404 Not Found: {str(error)}")
        return jsonify({
            "message": "Resource not found"
        }), 404

    # -------------------------------
    # 400 - Bad Request
    # -------------------------------
    @app.errorhandler(400)
    def handle_bad_request(error: Exception) -> ResponseReturnValue:
        app.logger.warning(f"400 Bad Request: {str(error)}")
        return jsonify({
            "message": "Bad request"
        }), 400

    # -------------------------------
    # 500 - Internal Server Error
    # -------------------------------

    @app.errorhandler(Exception)
    def handle_error(error: Exception) -> ResponseReturnValue:
        app.logger.exception(f'Handled error: {str(error)}')
        return jsonify({
            'message': str(error)
        }), 500