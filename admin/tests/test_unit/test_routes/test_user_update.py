from admin.tests.config import LOGIN, PASSWORD
from admin.models import MongoUser


def test_get_update_user(app):
    app.authorize(LOGIN, PASSWORD)
    user = MongoUser.objects(username=LOGIN).first()
    response = app.get_update_user(user.id)
    assert b'User updating form' in response.data
