from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories.user_repository_impl import UserRepositoryImpl

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

user_repository = UserRepositoryImpl()
auth_service = AuthService(user_repository)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    user = auth_service.register_user(username, email, password)
    if not user:
        return jsonify({'message': 'User already exists'}), 400

    access_token, refresh_token = auth_service.generate_tokens(user)
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400

    user = auth_service.authenticate_user(email, password)
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token, refresh_token = auth_service.generate_tokens(user)
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    access_token = auth_service.create_access_token(identity=current_user_id)
    return jsonify({'access_token': access_token}), 200
