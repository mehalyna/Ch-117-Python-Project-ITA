import os

import pytest
from mongoengine import disconnect, connect

from admin.app import create_app
from admin.tests.test_unit.test_routes.app import App


@pytest.fixture
def client():
    disconnect()
    flask_app = create_app()
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client


@pytest.fixture
def db_client():
    disconnect()
    flask_app = create_app()
    disconnect()
    connect('test', host='mongomock://localhost')
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client


@pytest.fixture
def app(client):
    app = App(client)
    return app
