from django.test import TestCase

from ..models import MongoUser, DjangoUser


class MongoUserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = MongoUser()
        user.first_name = 'test'
        user.last_name = 'test'
        user.username = 'test_user'
        user.email = 'test_user@gmail.com'
        user.password = 'test1234'
        user.save()

    def test_get_user(self):
        user = MongoUser.objects(username='test_user').first()
        self.assertIsInstance(user, MongoUser)

    def test_get_user1(self):
        user = MongoUser.objects(username='test_user').first()
        self.assertEqual('test_user', user.username)

    def tearDown(self) -> None:
        MongoUser.objects(username='test_user').first().delete()


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
