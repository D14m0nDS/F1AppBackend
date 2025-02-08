from apscheduler.schedulers.background import BackgroundScheduler
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.repositories.tokens_repository_impl import TokenRepositoryImpl

limiter = Limiter(key_func=get_remote_address)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="*")
cache = Cache()

def schedule_tasks():
    scheduler = BackgroundScheduler()
    token_repository = TokenRepositoryImpl()

    scheduler.add_job(token_repository.remove_expired_refresh_tokens, 'interval', hours=12)
    scheduler.start()