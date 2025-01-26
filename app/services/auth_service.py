from email_validator import validate_email, EmailNotValidError
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import cache
from app.models.user_model import User
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from app.repositories.user_repository import UserRepositoryInterface as UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.revoked_tokens = set()

    def register_user(self, username, email, password):
        if User.query.filter((User.email == email) | (User.username == username)).first():
            return None

        password_hash = generate_password_hash(password)
        user = self.user_repository.create_user(username, email, password_hash)
        self.user_repository.save(user)
        return user

    def authenticate_user(self, email, password):
        attempt_key = f"login_attempts:{email}"
        attempts = cache.get(attempt_key) or 0

        if attempts >= 5:
            return None, 'account_locked'

        user = self.user_repository.find_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            cache.delete(attempt_key)
            return user, None
        else:
            cache.set(attempt_key, attempts + 1, timeout=900)
            return None, 'invalid_credentials'

    @staticmethod
    def generate_tokens(user):

        access_expires = timedelta(hours=1)
        refresh_expires = timedelta(days=30)

        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=access_expires
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),
            expires_delta=refresh_expires
        )

        return access_token, refresh_token

    @staticmethod
    def create_access_token(identity):

        access_expires = timedelta(hours=1)

        access_token = create_access_token(identity=identity, expires_delta=access_expires)

        return access_token

    def revoke_token(self, token):
        self.revoked_tokens.add(token)

    def is_token_revoked(self, token):
        return token in self.revoked_tokens

    def get_user_by_id(self, user_id):
        return self.user_repository.find_by_id(int(user_id))

    def verify_password(self, user, current_password):
        return check_password_hash(user.password_hash, current_password)

    def update_password(self, user, new_password):
        user.password_hash = generate_password_hash(new_password)
        self.user_repository.save(user)