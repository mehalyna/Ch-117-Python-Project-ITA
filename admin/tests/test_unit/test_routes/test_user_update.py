from http import HTTPStatus

from admin.tests.config import LOGIN, PASSWORD


def test_get_update_user(app):
    app.authorize(LOGIN, PASSWORD)
    response = app.get_update_user()
    assert HTTPStatus.OK == response.status_code
    assert b'User updating form' in response.data
