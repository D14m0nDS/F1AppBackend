from .auth_controller import auth_bp
from .f1_controller import f1_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(f1_bp)
