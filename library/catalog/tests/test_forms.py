from django.test import TestCase

from ..forms import ChangePasswordForm, EditProfileForm


class ChangePasswordFormTest(TestCase):
    def test_new_and_confirm_password_not_match(self):
        data = {
            'old_password': 'pass1234',
            'new_password': 'pass12345',
            'confirm_password': 'test1234'
        }
        form = ChangePasswordForm(data=data)
        self.assertFalse(form.is_valid())


class EditProfileFormTest(TestCase):
    def test_edit_profile_form_fields_labels(self):
        form = EditProfileForm()
        self.assertTrue(form.fields['firstname'].label == 'Firstname')
        self.assertTrue(form.fields['lastname'].label == 'Lastname')
        self.assertTrue(form.fields['email'].label == 'Email')
        self.assertTrue(form.fields['login'].label == 'Login')
