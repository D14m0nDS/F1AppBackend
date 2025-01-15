from flask import jsonify

def handle_value_error(error):
    return jsonify({"error": str(error)}), 400

def handle_unexpected_error(error):
    return jsonify({"error": "An unexpected error occurred."}), 500



def register_error_handlers(blueprint):
    blueprint.register_error_handler(ValueError, handle_value_error)
    blueprint.register_error_handler(Exception, handle_unexpected_error)