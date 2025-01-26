from app.models.user_model import User
from app.extensions import db
from app.repositories.user_repository import UserRepositoryInterface

class UserRepositoryImpl(UserRepositoryInterface):
    def find_by_id(self, user_id):
        return User.query.get(user_id)

    def find_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def find_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def create_user(self, username, email, password_hash):
        return User(username=username, email=email, password_hash=password_hash)

    def save(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def delete(self, user):
        db.session.delete(user)
        db.session.commit()
