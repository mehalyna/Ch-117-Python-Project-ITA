from admin.tests.config import LOGIN, PASSWORD
from admin.models import User


def test_get_update_user(app):
    app.authorize(LOGIN, PASSWORD)
    user = User.objects(login=LOGIN).first()
    response = app.get_update_user(user.id)
    assert b'User updating form' in response.data
