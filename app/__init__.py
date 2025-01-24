from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt, socketio
from app.controllers import register_blueprints
from app.utils.caching import set_up_caching

def create_app(config_class=Config):
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    set_up_caching(app)
    register_blueprints(app)
    return app
