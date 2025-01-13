from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

# Define the blueprint
test_bp = Blueprint('test', __name__, url_prefix='/test')

# Test route to verify the app is running
@test_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Pong!"}), 200

# Test route to echo back JSON payload
@test_bp.route('/echo', methods=['POST'])
def echo():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    return jsonify({"echoed_data": data}), 200

# JWT-protected test route
@test_bp.route('/secure-ping', methods=['GET'])
@jwt_required()
def secure_ping():
    return jsonify({"message": "Pong from a secure endpoint!"}), 200

# Example of a dynamic test route
@test_bp.route('/params/<param>', methods=['GET'])
def test_params(param):
    return jsonify({"received_param": param}), 200
