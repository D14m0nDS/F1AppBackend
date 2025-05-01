import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME")
    INSTANCE = os.getenv("INSTANCE_CONNECTION_NAME")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}"
        f"@/{DB_NAME}"
        f"?host=/cloudsql/{INSTANCE}"
        f"&sslmode=disable"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_VERIFY_SUB = False
    CORS_ORIGINS = [
        "http://localhost:5173",
        "http://localhost:5174"
    ]
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    CORS_ALLOW_HEADERS = ["Content-Type", "Authorization", "x-access-token", "Cache-Control", "X-Requested-With"]
    CORS_SUPPORTS_CREDENTIALS = True
