from django.test import TestCase

from ..forms import ChangePasswordForm, EditProfileForm, RegistrationForm
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


class RegistrationFormTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        user1 = MongoUser()
        user1.first_name = 'test_registration_firstname1'
        user1.last_name = 'test_registration_lastname1'
        user1.username = 'test_registration_username1'
        user1.email = 'test_registration_email1@example.com'
        user1.password = 'test1234'
        user1.save()

    def setUp(self) -> None:
        self.user1 = MongoUser.objects(email='test_registration_email1@example.com').first()
        self.data = {
            'firstname': 'John',
            'lastname': 'Wick',
            'email': 'john@gmail.com',
            'login': 'john1234',
            'password': 'user1234',
            'confirm_password': 'user1234',
        }

        self.form = RegistrationForm

    def test_valid_form(self):
        self.assertTrue(self.form(data=self.data).is_valid())

    def test_firstname_label(self):
        self.assertEqual(self.form().fields['firstname'].label, 'Firstname')

    def test_lastname_label(self):
        self.assertEqual(self.form().fields['lastname'].label, 'Lastname')

    def test_email_label(self):
        self.assertEqual(self.form().fields['email'].label, 'Email')

    def test_login_label(self):
        self.assertEqual(self.form().fields['login'].label, 'Login')

    def test_password_label(self):
        self.assertEqual(self.form().fields['password'].label, 'Password')

    def test_confirm_password_label(self):
        self.assertEqual(self.form().fields['confirm_password'].label, 'Confirm password')

    def test_firstname_blank(self):
        data = self.data
        data['firstname'] = ''
        self.assertEqual(self.form(data=data).errors['firstname'], ['This field is required.'])

    def test_firstname_profanity(self):
        data = self.data
        data['firstname'] = 'shit'
        self.assertEqual(self.form(data=data).errors['firstname'], ['Contains profanity'])

    def test_lastname_blank(self):
        data = self.data
        data['lastname'] = ''
        self.assertEqual(self.form(data=data).errors['lastname'], ['This field is required.'])

    def test_lastname_profanity(self):
        data = self.data
        data['lastname'] = 'shit'
        self.assertEqual(self.form(data=data).errors['lastname'], ['Contains profanity'])

    def test_email_blank(self):
        data = self.data
        data['email'] = ''
        self.assertEqual(self.form(data=data).errors['email'], ['This field is required.'])

    def test_email_invalid(self):
        data = self.data
        data['email'] = 'johngmail.com'
        self.assertEqual(self.form(data=data).errors['email'], ['Enter a valid email address.'])

    def test_email_profanity(self):
        data = self.data
        data['email'] = 'shit@example.com'
        self.assertEqual(self.form(data=data).errors['email'], ['Contains profanity'])

    def test_email_unique_validation(self):
        data = self.data
        data['email'] = self.user1.email
        self.assertEqual(self.form(data=data).errors['email'], ['Is already taken'])

    def test_username_blank(self):
        data = self.data
        data['login'] = ''
        self.assertEqual(self.form(data=data).errors['login'], ['This field is required.'])

    def test_username_invalid_length(self):
        data = self.data
        data['login'] = 'joh1'
        self.assertEqual(
            self.form(data=data).errors['login'], ['Ensure this value has at least 6 characters (it has 4).']
        )

    def test_username_profanity(self):
        data = self.data
        data['login'] = '1shit123'
        self.assertEqual(self.form(data=data).errors['login'], ['Contains profanity'])

    def test_username_unique_validation(self):
        data = self.data
        data['login'] = self.user1.username
        self.assertEqual(self.form(data=data).errors['login'], ['Is already taken'])

    def test_password_invalid(self):
        data = self.data
        data['password'] = 'joh123'
        self.assertEqual(
            self.form(data=data).errors['password'], ['Minimum 8 characters, at least 1 letter and 1 number']
        )

    def test_confirm_password(self):
        data = self.data
        data['confirm_password'] = '543584798375943'
        self.assertEqual(
            self.form(data=data).errors['confirm_password'], ['Minimum 8 characters, at least 1 letter and 1 number']
        )

    def test_passwords_doesnt_match(self):
        data = self.data
        data['password'] = 'user1234'
        data['confirm_password'] = 'user12345'
        self.assertEqual(self.form(data=data).errors['__all__'], ['Password and confirm password doesn\'t match'])

    def test_error_count(self):
        data = {
            'firstname': 'John',
            'lastname': '',
            'email': 'johngmail.com',
            'login': 'john1',
            'password': 'user',
            'confirm_password': 'user1234',
        }
        self.assertEqual(len(self.form(data=data).errors), 5)
