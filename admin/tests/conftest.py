import os

import pytest
from mongoengine import disconnect


from admin.app import create_app
from admin.tests.test_unit.test_routes.app import App


@pytest.fixture
def client():
    disconnect()
    flask_app = create_app('DB_NAME', 'MONGO_URL', 'PORT')
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client


@pytest.fixture
def db_client():
    disconnect()
    flask_app = create_app('TEST_DB_NAME', 'MONGO_URL', 'PORT')
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client


@pytest.fixture
def app(client):
    app = App(client)
    return app
