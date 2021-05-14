from django.test import TestCase
from mongoengine import disconnect, connect
from django.conf import settings

from ..models import MongoUser, DjangoUser


class MongoUserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        disconnect()
        connect('test', host='mongomock://localhost')
        user = MongoUser()
        user.first_name = 'test'
        user.last_name = 'test'
        user.username = 'test_user'
        user.email = 'test_user@gmail.com'
        user.password = 'test1234'
        user.save()

    def test_users_creation(self):
        user = MongoUser.objects(username='test_user').first()
        django_user = DjangoUser.objects.get(username='test_user')
        self.assertIsInstance(django_user, DjangoUser)
        self.assertIsInstance(user, MongoUser)

    def test_get_user1(self):
        user = MongoUser.objects(username='test_user').first()
        self.assertEqual('test_user', user.username)

    @classmethod
    def tearDownClass(cls):
        disconnect()
        connect(settings.DB_NAME, host=settings.MONGO_DATABASE_HOST)


class DjangoUserTest(TestCase):
    def setUp(self) -> None:
        user = DjangoUser()
        user.username = 'user_test'
        user.email = 'user_test@gmail.com'
        user.set_password('pass1234')
        user.save()

    def test_get_user(self):
        user = DjangoUser.objects.get(username='user_test')
        self.assertTrue(user.check_password('pass1234'))
