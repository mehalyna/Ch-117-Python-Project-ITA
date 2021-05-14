from django.test import TestCase

from ..models import MongoUser


class MongoUserTest(TestCase):
    @classmethod
    def setUpClass(cls):
        user = MongoUser()
        user.first_name = 'test'
        user.last_name = 'test'
        user.username = 'test_user'
        user.email = 'test_user1@gmail.com'
        user.password = 'test1234'
        user.save()

    def test_users_creation(self):
        user = MongoUser.objects(username='test_user').first()
        self.assertIsInstance(user, MongoUser)
