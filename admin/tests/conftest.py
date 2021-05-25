import os

import pytest
from mongoengine import disconnect, connect

from admin.app import create_app
from admin.tests.test_unit.test_routes.app import App
from admin.models import MongoUser
from admin.tests.config import (
    EMAIL, LOGIN, LAST_NAME, FIRST_NAME, PASSWORD, ROLE
)


@pytest.fixture(scope='session')
def flask_app():
    app = create_app()
    disconnect()
    connect('test', host='mongomock://localhost')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app


@pytest.fixture(scope='session')
def flask_app_with_admin(flask_app):
    u = MongoUser()
    u.firstname = FIRST_NAME
    u.lastname = LAST_NAME
    u.email = EMAIL
    u.username = LOGIN
    u.role = ROLE
    u.is_admin = True
    u.set_password(PASSWORD)
    u.save()
    return flask_app


@pytest.fixture(scope='session')
def client(flask_app_with_admin):
    with flask_app_with_admin.test_client() as client:
        with flask_app_with_admin.app_context():
            yield client


@pytest.fixture(scope='session')
def app(client):
    app = App(client)
    return app
