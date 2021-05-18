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


class RegistrationPageTest(TestCase):
    def setUp(self) -> None:
        self.registration_url = reverse('library-registration')

    def test_get_page(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)

    def test_post_page(self):
        data = {
            'firstname': 'John',
            'lastname': 'Wick',
            'email': 'john45654645@gmail.com',
            'login': 'john123453464',
            'password': 'user1234',
            'confirm_password': 'user1234'
        }
        response = self.client.post(self.registration_url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
