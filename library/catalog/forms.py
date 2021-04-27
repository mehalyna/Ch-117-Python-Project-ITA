from bson import ObjectId
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import CharField, EmailField, Form, PasswordInput, TextInput
from mongoengine.queryset.visitor import Q

from .models import User

PASSWORD_PATTERN = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
PASSWORD_MESSAGE = 'Minimum 8 characters, at least 1 letter and 1 number'


def unique_check(value):
    message = f'Is already taken'
    user = User.objects(Q(login=value) | Q(email=value))
    if user:
        raise ValidationError(message)


class RegistrationForm(Form):
    firstname = CharField(label='Firstname', max_length=100,
                          widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}))
    lastname = CharField(label='Lastname', max_length=100,
                         widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Wick'}))
    email = EmailField(label='Email', max_length=100, validators=[unique_check],
                       widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'john@example.com'}))
    login = CharField(label='Login', min_length=6, max_length=100, validators=[unique_check],
                      widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'johny_1234'}))
    password = CharField(label='Password', max_length=100,
                         validators=[RegexValidator(regex=PASSWORD_PATTERN, message=PASSWORD_MESSAGE)],
                         widget=PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = CharField(label='Confirm password', max_length=100,
                                 validators=[RegexValidator(regex=PASSWORD_PATTERN, message=PASSWORD_MESSAGE)],
                                 widget=PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('Password and confirm password doesn\'t match')


class EditProfileForm(Form):
    user = User.objects(id='606ecd74e5fd490b3c6d0657').first()  # for autofill data session user
    user_id = CharField(required=False, widget=TextInput(attrs={'value': user.id}))
    firstname = CharField(label='Firstname', max_length=100,
                          widget=TextInput(attrs={'class': 'form-control', 'value': user.firstname}))
    lastname = CharField(label='Lastname', max_length=100,
                         widget=TextInput(attrs={'class': 'form-control', 'value': user.lastname}))
    email = EmailField(label='Email', max_length=100,
                       widget=TextInput(attrs={'class': 'form-control', 'value': user.email}))
    login = CharField(label='Login', min_length=6, max_length=100,
                      widget=TextInput(attrs={'class': 'form-control', 'value': user.login}))


class ChangePasswordForm(Form):
    old_password = CharField(label='Old password', max_length=100,
                             validators=[RegexValidator(regex=PASSWORD_PATTERN, message=PASSWORD_MESSAGE)],
                             widget=PasswordInput(attrs={'class': 'form-control'}))
    new_password = CharField(label='New password', max_length=100,
                         validators=[RegexValidator(regex=PASSWORD_PATTERN, message=PASSWORD_MESSAGE)],
                         widget=PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = CharField(label='Confirm password', max_length=100,
                                 validators=[RegexValidator(regex=PASSWORD_PATTERN, message=PASSWORD_MESSAGE)],
                                 widget=PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('Password and confirm password doesn\'t match')
