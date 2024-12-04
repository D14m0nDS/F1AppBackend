from abc import ABC, abstractmethod


class UserRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, user_id):
        pass

    @abstractmethod
    def find_by_email(self, email):
        pass

    @abstractmethod
    def find_by_username(self, username):
        pass

    @abstractmethod
    def create_user(self, username, email, password_hash):
        pass

    @abstractmethod
    def save(self, user):
        pass

    @abstractmethod
    def delete(self, user):
        pass
