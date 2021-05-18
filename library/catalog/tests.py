from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class BaseTest(TestCase):
    def setUp(self):
        self.login_url = reverse('func_login')
        self.login_redirect_page = reverse('login_redirect_page')
        self.user = {
            'username': 'testemail@gmail.com',
            'password': 'Test123'
        }


class LoginTest(BaseTest):
    def test_can_access_redirect_page(self):
        response = self.client.get(self.login_redirect_page)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_redirect.html')

    def test_login_success(self):
        self.client.post(self.login_url)