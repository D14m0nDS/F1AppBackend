from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt, socketio
from app.controllers import register_blueprints
from app.utils.caching import cache


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    cache.init_app(app)

    register_blueprints(app)

    return app
