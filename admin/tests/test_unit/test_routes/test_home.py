from http import HTTPStatus

from admin.tests.config import LOGIN, PASSWORD


def test_get_home(app):
    app.authorize(LOGIN, PASSWORD)
    response = app.get_home()
    assert HTTPStatus.OK == response.status_code
    assert b'Welcome to administrator panel' in response.data
