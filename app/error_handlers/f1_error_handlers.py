from flask import jsonify
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound, MethodNotAllowed, InternalServerError


def handle_bad_request(_error):
    return jsonify({"error": "Bad request"}), 400


def handle_unauthorized(_error):
    return jsonify({"error": "Unauthorized"}), 401


def handle_forbidden(_error):
    return jsonify({"error": "Forbidden"}), 403


def handle_not_found(_error):
    return jsonify({"error": "Resource not found"}), 404


def handle_method_not_allowed(_error):
    return jsonify({"error": "Method not allowed"}), 405


def handle_internal_server_error(_error):
    return jsonify({"error": "Internal server error"}), 500


def register_error_handlers(app):
    app.register_error_handler(BadRequest, handle_bad_request)
    app.register_error_handler(Unauthorized, handle_unauthorized)
    app.register_error_handler(Forbidden, handle_forbidden)
    app.register_error_handler(NotFound, handle_not_found)
    app.register_error_handler(MethodNotAllowed, handle_method_not_allowed)
    app.register_error_handler(InternalServerError, handle_internal_server_error)
