from django.test import TestCase
from django.urls import reverse

from catalog.models import MongoUser


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


class RedirectLoginTest(TestCase):

    def setUp(self) -> None:
        self.login_redirect_page = reverse('login_redirect_page')

    def test_can_access_redirect_page(self):
        response = self.client.get(self.login_redirect_page)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_redirect.html')