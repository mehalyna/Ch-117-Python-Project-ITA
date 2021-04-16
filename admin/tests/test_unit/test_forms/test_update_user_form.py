from admin.tests.config import LOGIN, PASSWORD
from admin.forms import UpdateUserForm


def test_update_user_form_without_password(app):
    app.authorize(LOGIN, PASSWORD)
    data = {
        'firstname': 'TestName',
        'lastname': 'TestLastname',
        'email': 'test@ex.com',
        'login': 'test1234',
        'role': 'user',
        'status': 'active'
    }
    response = UpdateUserForm(data=data)
    assert not response.validate()


def test_update_user_form_without_data(app):
    app.authorize(LOGIN, PASSWORD)
    data = {}
    response = UpdateUserForm(data=data)
    assert not response.validate()
