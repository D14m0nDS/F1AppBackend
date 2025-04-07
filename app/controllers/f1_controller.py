import os

from flask import Blueprint, jsonify, request, send_from_directory, current_app
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
@cache.cached(timeout=3600, query_string=True)
def get_driver_standings():
    season = request.args.get('season', type=str)

    if not season:
        return jsonify({"error": "Missing required parameter 'season'"}), 400

    if season == "current":
        season = 2024
    else:
        season = int(season)

    try:
        standings = f1_service.get_driver_standings(season)
        return jsonify(standings), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to retrieve standings" + e.__str__()}), 500


@f1_bp.route('/standings/constructors', methods=['GET'])
@cache.cached(timeout=3600, query_string=True)
def get_constructor_standings():
    season = request.args.get('season', type=str)

    if not season:
        return jsonify({"error": "Missing required parameter 'season'"}), 400

    if season == "current":
        season = 2024
    else:
        season = int(season)

    try:
        standings = f1_service.get_constructor_standings(season)
        return jsonify(standings), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to retrieve standings" + e.__str__()}), 500

@f1_bp.route('/schedule', methods=['GET'])
@cache.cached(timeout=3600)
def get_schedule():
    schedule = f1_service.get_schedule()
    return jsonify(schedule), 200

@f1_bp.route('/race', methods=['GET'])
@cache.cached(timeout=1800, query_string=True)
def get_race():

    season = request.args.get('season', type=str)
    round = request.args.get('round', type=int)
    if not season or not round:
        return jsonify({"error": "Missing required parameters 'season' and 'round'"}), 400

    if season == "current":
        season = 2024
    else:
        season = int(season)

    try:
        race = f1_service.get_race(season, round)
        return jsonify(race), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred." + e.__str__()}), 500


@f1_bp.route('/driver', methods=['GET'])
@cache.cached(timeout=1800, query_string=True)
def get_driver():
    driver_id = request.args.get('id', type=str)

    if not driver_id:
        return jsonify({"error": "Missing required parameter 'id'"}), 400

    driver = f1_service.get_driver(driver_id)
    return jsonify(driver)

@f1_bp.route('/constructor', methods=['GET'])
@cache.cached(timeout=1800, query_string=True)
def get_constructor():
    constructor_id = request.args.get('id', type=str)

    if not constructor_id:
        return jsonify({"error": "Missing required parameter 'id'"}), 400

    constructor = f1_service.get_constructor(constructor_id)
    return jsonify(constructor)

@f1_bp.route('/drivers', methods=['GET'])
@cache.cached(timeout=1800, query_string=True)
def get_all_drivers():
    season = request.args.get('season', type=str)

    if not season:
        return jsonify({"error": "Missing required parameter 'season'"}), 400

    if season == "current":
        season = 2024
    else :
        season = int(season)

    drivers = f1_service.get_all_drivers(season)
    return jsonify(drivers)

@f1_bp.route('/constructors', methods=['GET'])
@cache.cached(timeout=1800, query_string=True)
def get_all_constructors():
    season = request.args.get('season', type=str)

    if not season:
        return jsonify({"error": "Missing required parameter 'season'"}), 400

    if season == "current":
        season = 2024
    else :
        season = int(season)

    constructors = f1_service.get_all_constructors(season)

    return jsonify(constructors)


@f1_bp.route('/images/<filename>', methods=['GET'])
def serve_image(filename):
    image_folder = os.path.join(current_app.root_path, 'static/images')

    if not os.path.exists(os.path.join(image_folder, filename)):
        return jsonify({"error": "Image not found"}), 404

    return send_from_directory(image_folder, filename)

register_error_handlers(f1_bp)