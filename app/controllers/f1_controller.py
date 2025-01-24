from flask import Blueprint, jsonify, request
from app.error_handlers.f1_error_handlers import register_error_handlers
from app.repositories.driver_repository_impl import DriverRepositoryImpl
from app.repositories.constructor_repository_impl import ConstructorRepositoryImpl
from app.repositories.race_repository_impl import RaceRepositoryImpl
from app.services.f1_service import F1Service
from app.extensions import cache


f1_bp = Blueprint('f1', __name__, url_prefix='/f1')

driver_repository = DriverRepositoryImpl()
constructor_repository = ConstructorRepositoryImpl()
race_repository = RaceRepositoryImpl()

f1_service = F1Service(driver_repository, constructor_repository, race_repository)

@f1_bp.route('/standings/drivers', methods=['GET'])
@cache.cached(timeout=3600)
def get_driver_standings():
    standings = "1.Max"

    return jsonify(standings), 200


@f1_bp.route('/standings/constructors', methods=['GET'])
@cache.cached(timeout=3600)
def get_constructor_standings():
    standings = "McLaren"
    return jsonify(standings), 200

@f1_bp.route('/schedule', methods=['GET'])
@cache.cached(timeout=3600)
def get_schedule():
    schedule = f1_service.get_schedule()
    return jsonify(schedule), 200

@f1_bp.route('/race', methods=['GET'])
def get_race():

    season = request.args.get('season', type=int)
    round = request.args.get('round', type=int)
    if not season or not round:
        return jsonify({"error": "Missing required parameters 'season' and 'round'"}), 400

    try:
        race = f1_service.get_race(season, round)
        return jsonify(race), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500


@f1_bp.route('/driver', methods=['GET'])
def get_driver():
    driver_id = request.args.get('id', type=int)

    if not driver_id:
        return jsonify({"error": "Missing required parameter 'id'"}), 400

    driver = f1_service.get_driver(driver_id)
    return jsonify(driver)

@f1_bp.route('/constructor', methods=['GET'])
def get_constructor():
    constructor_id = request.args.get('id', type=int)

    if not constructor_id:
        return jsonify({"error": "Missing required parameter 'id'"}), 400

    constructor = f1_service.get_constructor(constructor_id)
    return jsonify(constructor)

@f1_bp.route('/drivers', methods=['GET'])
@cache.cached(timeout=1800)
def get_all_drivers():
    drivers = f1_service.get_all_drivers()
    return jsonify(drivers)

@f1_bp.route('/constructors', methods=['GET'])
@cache.cached(timeout=1800)
def get_all_constructors():
    constructors = f1_service.get_all_constructors()
    return jsonify(constructors)

register_error_handlers(f1_bp)