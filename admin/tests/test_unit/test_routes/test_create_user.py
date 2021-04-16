from http import HTTPStatus

from admin.tests.config import CREATE_VALID_USER, CREATE_INVALID_USER, LOGIN, PASSWORD


def test_get_create_user(app):
    app.authorize(LOGIN, PASSWORD)
    response = app.get_user_create()
    assert HTTPStatus.OK == response.status_code
    assert b'User adding form' in response.data


def test_post_create_valid_user(app):
    app.authorize(LOGIN, PASSWORD)
    response = app.post_user_create(CREATE_VALID_USER)
    assert b'User List' in response.data


def test_post_create_invalid_user(app):
    app.authorize(LOGIN, PASSWORD)
    response = app.post_user_create(CREATE_INVALID_USER)
    assert b'User adding form' in response.data
