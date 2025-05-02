import os
import pytest
from app import create_app
from app.extensions import db as _db
from flask_migrate import upgrade as migrate_up

@pytest.fixture(scope='session')
def app():
    os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@localhost:5432/testdb'
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ['DATABASE_URL'],
        "JWT_SECRET_KEY": "super-secret-test-key",
    })
    with app.app_context():
        migrate_up()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    return _db

@pytest.fixture
def access_token(app):
    from flask_jwt_extended import create_access_token
    with app.app_context():
        return create_access_token(identity="test-user")
