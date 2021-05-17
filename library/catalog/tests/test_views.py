from django.test import TestCase


class HomePageTest(TestCase):
    def test_get_page(self):
        response = self.client.get('/library/home/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Popular books of the week', response.content)

    def test_context(self):
        response = self.client.get('/library/home/')
        self.assertEqual([], response.context['top_books'])


class ProfileEditViewTest(TestCase):
    def test_unauthorized_get_page(self):
        response = self.client.get('/library/profile_edit/')
        self.assertEqual(response.status_code, 302)


