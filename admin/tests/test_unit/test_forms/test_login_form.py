
from admin.forms import LoginForm


def test_login_form(client):
    form = LoginForm(data={'admin': 'testing', 'password': 'testtest'})
    assert form.validate()


def test_login_form_with_invalid_short_data(client):
    form = LoginForm(data={'admin': '123456', 'password': '1234567'})
    assert not form.validate()

    form = LoginForm(data={'admin': '12345', 'password': '12345678'})
    assert not form.validate()


def test_login_form_with_no_data(client):
    form = LoginForm(data={})
    assert not form.validate()


