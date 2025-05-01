from email_validator import validate_email, EmailNotValidError
from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from markupsafe import escape
from app import limiter
from app.services.auth_service import AuthService
from app.repositories.user_repository_impl import UserRepositoryImpl
from app.repositories.tokens_repository_impl import TokenRepositoryImpl

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService(UserRepositoryImpl(), TokenRepositoryImpl())

@auth_bp.route('/register', methods=['POST'])
def register():
    username, email, password, password_confirmation = extract_register_data(request.get_json())

    if not all([username, email, password, password_confirmation]):
        return jsonify({'message': 'Missing required fields'}), 400

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
    email, password = extract_login_data(request.get_json())

    if not all([email, password]):
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        validate_email(email).normalized
    except EmailNotValidError:
        return jsonify({'message': 'Invalid email format'}), 400

    user, error = auth_service.authenticate_user(email, password)

    if error == 'account_locked':
        return jsonify({'message': 'Account locked for 5 minutes'}), 429
    elif not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token, refresh_token = auth_service.generate_tokens(user)
    session['user_id'] = user.id
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required(refresh=True)
def logout():
    refresh_jti = get_jwt().get("jti")
    auth_service.revoke_refresh_token(refresh_jti)
    return jsonify({'message': 'Refresh token revoked successfully'}), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    jti = get_jwt()["jti"]

    if auth_service.is_refresh_token_revoked(jti):
        return jsonify({"message": "Token has been revoked"}), 401

    if not auth_service.is_refresh_token_active(jti):
        return jsonify({"message": "Token not active"}), 401


    current_user_id = get_jwt_identity()


    user = auth_service.get_user_by_id(int(current_user_id))

    new_access_token, new_refresh_token = auth_service.generate_tokens(user)
    auth_service.revoke_refresh_token(jti)

    return jsonify({
        'access_token': new_access_token,
        'refresh_token': new_refresh_token
    }), 200


# @auth_bp.route('/change-password', methods=['POST'])
# @jwt_required()
# def change_password():
#     data = request.get_json()
#     current_password = data.get('current_password')
#     new_password = data.get('new_password')
#     new_password_confirmation = data.get('new_password_confirmation')
#
#     if not all([current_password, new_password, new_password_confirmation]):
#         return jsonify({'message': 'Missing required fields'}), 400
#
#     if new_password != new_password_confirmation:
#         return jsonify({'message': 'New passwords do not match'}), 400
#
#     current_user_id = get_jwt_identity()
#     user = auth_service.get_user_by_id(current_user_id)
#     if not user:
#         return jsonify({'message': 'User not found'}), 404
#
#     if not auth_service.verify_password(user, current_password):
#         return jsonify({'message': 'Current password is incorrect'}), 401
#
#     auth_service.update_password(user, new_password)
#
#     access_token, refresh_token = auth_service.generate_tokens(user)
#     return jsonify({
#         'message': 'Password updated successfully',
#         'access_token': access_token,
#         'refresh_token': refresh_token
#     }), 200

def extract_register_data(data: dict):
    username_raw = data["username"]
    email_raw = data["email"]
    password_raw = data["password"]
    password_confirmation_raw = data["password_confirmation"]

    if not all([username_raw, email_raw, password_raw, password_confirmation_raw]):
        return None, None, None, None

    username = escape(username_raw.strip())
    email = escape(email_raw.strip().lower())
    password = escape(password_raw.strip())
    password_confirmation = escape(password_confirmation_raw.strip())
    return username, email, password, password_confirmation

def extract_login_data(data: dict):
    email_raw = data.get('email')
    password_raw = data.get('password')
    if not all([email_raw, password_raw]):
        return None, None

    email    = escape(email_raw.strip().lower())
    password = escape(password_raw.strip())
    return email, password