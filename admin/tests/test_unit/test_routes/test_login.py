from http import HTTPStatus


def test_get_admin_login(app):
    response = app.get_login()
    assert HTTPStatus.OK == response.status_code
    assert b'Sign In' in response.data
