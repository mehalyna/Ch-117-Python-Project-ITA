from django.test import TestCase
from django.urls import reverse

from ..models import MongoUser


class HomePageTest(TestCase):
    def test_get_page(self):
        response = self.client.get('/library/home/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Popular books of the week', response.content)

    def test_context(self):
        response = self.client.get('/library/home/')
        self.assertEqual([], response.context['top_books'])


class ProfileEditViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        user = MongoUser()
        user.first_name = 'test_firstname'
        user.last_name = 'test_lastname'
        user.username = 'test_username'
        user.email = 'test_email@example.com'
        user.password = 'test1234'
        user.save()

    def setUp(self) -> None:
        self.profile_edit_url = reverse('profile_edit')

    def test_unauthorized_get_page(self):
        response = self.client.get(self.profile_edit_url)
        self.assertEqual(response.status_code, 302)

    def test_redirect_unauthorized(self):
        response = self.client.get(self.profile_edit_url)
        self.assertRedirects(response, (reverse('login_redirect_page') + '?next=' + reverse('profile_edit')))

    def test_get_page(self):
        self.client.login(username='test_username', password='test1234')
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit profile', response.content)


class LoginViewTest(TestCase):
    def setUp(self) -> None:
        user = MongoUser()
        user.first_name = 'test'
        user.last_name = 'test'
        user.username = 'testing'
        user.email = 'test@gmail.com'
        user.password = 'test1234'
        self.user = user.save()

    def tearDown(self) -> None:
        self.user.delete()

    def test_login_with_valid_data(self):
        data = {
            'username': 'testing',
            'password': 'test1234'
        }
        response = self.client.post('/library/func_login', data=data)
        self.assertIn(b'Success', response.content)

    def test_login_with_invalid_username(self):
        data = {
            'username': 'not_exist_username',
            'password': 'test1234'
        }
        response = self.client.post('/library/func_login', data=data)
        self.assertIn(b'Denied', response.content)

    def test_login_with_invalid_password(self):
        data = {
            'username': 'testing',
            'password': 'invalid_pass'
        }
        response = self.client.post('/library/func_login', data=data)
        self.assertIn(b'Denied', response.content)
