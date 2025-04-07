from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt, socketio, limiter, cors
from app.controllers import register_blueprints
from app.utils.caching import set_up_caching

def create_app(config_class=Config):
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config.from_object(config_class)

    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax'
    )

    cors.init_app(app, resources={
        r"/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": app.config['CORS_METHODS'],
            "allow_headers": app.config['CORS_ALLOW_HEADERS'],
            "supports_credentials": app.config['CORS_SUPPORTS_CREDENTIALS'],
            "expose_headers": ["Content-Type", "Authorization"]
        },
    })

    db.init_app(app)

    from app.models.user_model import User
    from app.models.revoked_refresh_token_model import RevokedRefreshToken
    from app.models.revoked_access_token_model import RevokedAccessToken
    from app.models.active_token_model import ActiveRefreshToken

    migrate.init_app(app, db)

    limiter.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    set_up_caching(app)
    register_blueprints(app)

    return app
