from abc import ABC, abstractmethod

class  TokenRepositoryInterface(ABC):
    @abstractmethod
    def store_revoked_access_token(self, jti):
        pass

    @abstractmethod
    def is_access_token_revoked(self, jti):
        pass

    @abstractmethod
    def store_revoked_refresh_token(self, jti):
        pass

    @abstractmethod
    def is_refresh_token_revoked(self, jti):
        pass

    @abstractmethod
    def create_active_refresh_token(self, user_id, jti, expires_at):
        pass

    @abstractmethod
    def is_refresh_token_active(self, jti):
        pass

    @abstractmethod
    def delete_active_refresh_token(self, jti):
        pass

    @abstractmethod
    def remove_expired_refresh_tokens(self):
        pass