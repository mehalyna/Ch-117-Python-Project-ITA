
from admin.forms import AddUserForm
from admin.tests.config import CREATE_VALID_USER, CREATE_INVALID_USER, CREATE_LOGGED_USER


def test_create_user_form(client):
    form = AddUserForm(data=CREATE_VALID_USER)
    assert form.validate()


def test_create_user_form_with_invalid_data(client):
    form = AddUserForm(data=CREATE_INVALID_USER)
    assert not form.validate()


def test_create_user_form_with_no_data(client):
    form = AddUserForm(data={})
    assert not form.validate()


def test_create_user_form_unique(client):
    form = AddUserForm(data=CREATE_LOGGED_USER)
    assert not form.validate()
