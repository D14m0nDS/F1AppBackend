from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_model import User
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from app.repositories.user_repository import UserRepositoryInterface as UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, username, email, password):
        if User.query.filter((User.email == email) | (User.username == username)).first():
            return None

        password_hash = generate_password_hash(password)
        user = self.user_repository.create_user(username, email, password_hash)

        self.user_repository.save(user)

        return user

    def authenticate_user(self, email, password):
        user = self.user_repository.find_by_email(email)

        if user and check_password_hash(user.password_hash, password):
            return user

        return None

    @staticmethod
    def generate_tokens(user):

        access_expires = timedelta(hours=1)
        refresh_expires = timedelta(days=30)

        access_token = create_access_token(identity=user.id, expires_delta=access_expires)
        refresh_token = create_refresh_token(identity=user.id, expires_delta=refresh_expires)

        return access_token, refresh_token

    @staticmethod
    def create_access_token(identity):

        access_expires = timedelta(hours=1)

        access_token = create_access_token(identity=identity, expires_delta=access_expires)

        return access_token
