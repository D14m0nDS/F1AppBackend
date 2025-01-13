from flask import Blueprint, jsonify, request
from app.services.f1_service import F1Service

f1_bp = Blueprint('f1', __name__, url_prefix='/f1')


@f1_bp.route('/standings/drivers', methods=['GET'])
def get_driver_standings():
    standings = F1Service.get_driver_standings()
    return jsonify(standings), 200


@f1_bp.route('/standings/constructors', methods=['GET'])
def get_constructor_standings():
    standings = F1Service.get_constructor_standings()
    return jsonify(standings), 200

@f1_bp.route('/schedule', methods=['GET'])
def get_schedule():
    schedule = F1Service.get_schedule()
    return jsonify(schedule), 200

@f1_bp.route('/race', methods=['GET'])
def get_race():
    year = request.args.get('year', type=int)
    round = request.args.get('round', type=int)

    if not year or not round:
        return jsonify({"error": "Missing required parameters 'year' and 'round'"}), 400

    race = F1Service.get_race(year, round)
    return jsonify(race)


@f1_bp.route('/driver', methods=['GET'])
def get_driver():
    driver_id = request.args.get('id', type=int)

    if not driver_id:
        return jsonify({"error": "Missing required parameter 'id'"}), 400

    driver = F1Service.get_driver(driver_id)
    return jsonify(driver)

@f1_bp.route('/constructor', methods=['GET'])
def get_constructor():
    constructor_id = request.args.get('id', type=int)

    if not constructor_id:
        return jsonify({"error": "Missing required parameter 'id'"}), 400

    constructor = F1Service.get_constructor(constructor_id)
    return jsonify(constructor)

@f1_bp.route('/drivers', methods=['GET'])
def get_all_drivers():
    drivers = F1Service.get_all_drivers()
    return jsonify(drivers)

@f1_bp.route('/constructors', methods=['GET'])
def get_all_constructors():
    constructors = F1Service.get_all_constructors()
    return jsonify(constructors)