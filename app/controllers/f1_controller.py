from flask import Blueprint, jsonify
from app.services.f1_service import F1Service
from flask_jwt_extended import jwt_required

f1_bp = Blueprint('f1', __name__, url_prefix='/f1')

@f1_bp.route('/standings/drivers', methods=['GET'])
@jwt_required()
def get_driver_standings():
    standings = F1Service.get_driver_standings()
    return jsonify(standings), 200

@f1_bp.route('/standings/constructors', methods=['GET'])
@jwt_required()
def get_constructor_standings():
    standings = F1Service.get_constructor_standings()
    return jsonify(standings), 200

# Add more routes as needed
