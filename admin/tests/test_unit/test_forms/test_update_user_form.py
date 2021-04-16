from admin.tests.config import LOGIN, PASSWORD
from admin.forms import UpdateUserForm


def test_update_user_form_without_password(app):
    app.authorize(LOGIN, PASSWORD)
    data = {
        'firstname': 'Taras',
        'lastname': 'Shyichuk',
        'email': 'taras@ex.com',
        'login': 'taras0024',
        'role': 'admin',
        'status': 'active'
    }
    response = UpdateUserForm(data=data)
    assert not response.validate()


def test_update_user_form_without_data(app):
    app.authorize(LOGIN, PASSWORD)
    data = {}
    response = UpdateUserForm(data=data)
    assert not response.validate()