from django.test import TestCase, Client
from django.urls import reverse

from ..models import DjangoUser, MongoUser


class HomePageTest(TestCase):
    def test_get_page(self):
        response = self.client.get('/library/home/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Popular books of the week', response.content)

    def test_context(self):
        response = self.client.get('/library/home/')
        self.assertEqual([], response.context['top_books'])


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
