from django.test import TestCase

from ..forms import ChangePasswordForm


class ChangePasswordFormTest(TestCase):
    def test_new_and_confirm_password_not_match(self):
        data = {
            'old_password': 'pass1234',
            'new_password': 'pass12345',
            'confirm_password': 'test1234'
        }
        form = ChangePasswordForm(data=data)
        self.assertFalse(form.is_valid())
