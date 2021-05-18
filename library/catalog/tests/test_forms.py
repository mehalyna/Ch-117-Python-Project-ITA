from django.test import TestCase

from ..forms import ChangePasswordForm, EditProfileForm
from ..models import MongoUser


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
    @classmethod
    def setUpClass(cls):
        user1 = MongoUser()
        user1.first_name = 'test_firstname'
        user1.last_name = 'test_lastname'
        user1.username = 'test_usernameform1'
        user1.email = 'test_emailform1@example.com'
        user1.password = 'test1234'
        user1.save()

        user2 = MongoUser()
        user2.first_name = 'test_firstname'
        user2.last_name = 'test_lastname'
        user2.username = 'test_usernameform2'
        user2.email = 'test_emailform2@example.com'
        user2.password = 'test1234'
        user2.save()

    def test_edit_profile_form_firstname_label(self):
        form = EditProfileForm()
        self.assertTrue(form.fields['firstname'].label == 'Firstname')

    def test_edit_profile_form_lastname_label(self):
        form = EditProfileForm()
        self.assertTrue(form.fields['lastname'].label == 'Lastname')

    def test_edit_profile_form_email_label(self):
        form = EditProfileForm()
        self.assertTrue(form.fields['email'].label == 'Email')

    def test_edit_profile_form_login_label(self):
        form = EditProfileForm()
        self.assertTrue(form.fields['login'].label == 'Login')

    def test_form_email_unique_validation(self):
        user1 = MongoUser.objects(username='test_usernameform1').first()
        user2 = MongoUser.objects(username='test_usernameform2').first()
        form = EditProfileForm(data={
            'user_id': user2.id,
            'firstname': user2.first_name,
            'lastname': user2.last_name,
            'email': user1.email,
            'login': user2.username
        })
        self.assertEqual(form.errors['email'], ['is already taken'])

    def test_form_error_count(self):
        form = EditProfileForm(data={
            'user_id': '609266773881afe4b7709f2f',
            'firstname': '',
            'lastname': '',
            'email': '',
            'login': 'login1234'
        })
        self.assertEqual(len(form.errors), 3)
