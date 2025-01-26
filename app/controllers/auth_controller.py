from email_validator import validate_email, EmailNotValidError
from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from markupsafe import escape
from app import limiter
from app.services.auth_service import AuthService
from app.repositories.user_repository_impl import UserRepositoryImpl

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService(UserRepositoryImpl())

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username_raw = data.get('username')
    email_raw = data.get('email')
    password_raw = data.get('password')
    password_confirmation_raw = data.get('password_confirmation')

    if not all([username_raw, email_raw, password_raw, password_confirmation_raw]):
        return jsonify({'message': 'Missing required fields'}), 400

    username = escape(username_raw.strip())
    email = escape(email_raw.strip().lower())
    password = escape(password_raw.strip())
    password_confirmation = escape(password_confirmation_raw.strip())
    if password != password_confirmation:
        return jsonify({'message': 'Passwords do not match'}), 400
    try:
        validate_email(email).normalized
    except EmailNotValidError:
        return jsonify({'message': 'Invalid email format'}), 400

    user = auth_service.register_user(username, email, password)
    if not user:
        return jsonify({'message': 'User already exists'}), 400

    access_token, refresh_token = auth_service.generate_tokens(user)
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 201

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5/minute")
def login():
    data = request.get_json()
    email_raw = data.get('email')
    password_raw = data.get('password')

    if not all([email_raw, password_raw]):
        return jsonify({'message': 'Missing required fields'}), 400

    email = escape(email_raw.strip().lower())
    password = escape(password_raw.strip())

    try:
        validate_email(email).normalized
    except EmailNotValidError:
        return jsonify({'message': 'Invalid email format'}), 400

    user, error = auth_service.authenticate_user(email, password)
    if error == 'account_locked':
        return jsonify({'message': 'Account locked for 15 minutes'}), 429
    elif not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token, refresh_token = auth_service.generate_tokens(user)
    session['user_id'] = user.id
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    auth_service.revoke_token(jti)
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    user = auth_service.get_user_by_id(int(current_user_id))
    access_token = auth_service.generate_tokens(user)[0]
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    new_password_confirmation = data.get('new_password_confirmation')

    if not all([current_password, new_password, new_password_confirmation]):
        return jsonify({'message': 'Missing required fields'}), 400

    if new_password != new_password_confirmation:
        return jsonify({'message': 'New passwords do not match'}), 400

    current_user_id = get_jwt_identity()
    user = auth_service.get_user_by_id(current_user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if not auth_service.verify_password(user, current_password):
        return jsonify({'message': 'Current password is incorrect'}), 401

    auth_service.update_password(user, new_password)

    access_token, refresh_token = auth_service.generate_tokens(user)
    return jsonify({
        'message': 'Password updated successfully',
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200
