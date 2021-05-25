from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import CharField, EmailField, Form, PasswordInput, TextInput
from mongoengine.queryset.visitor import Q
from profanityfilter import ProfanityFilter

from .models import MongoUser

PASSWORD_MESSAGE = 'Minimum 8 characters, at least 1 letter and 1 number'
PASSWORD_PATTERN = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
pf = ProfanityFilter(no_word_boundaries=True)


def profanity_check(value):
    message = 'Contains profanity'
    if not pf.is_clean(value):
        raise ValidationError(message)


class RegistrationForm(Form):
    firstname = CharField(label='Firstname', max_length=100, validators=[profanity_check],
                          widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}))
    lastname = CharField(label='Lastname', max_length=100, validators=[profanity_check],
                         widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Wick'}))
    email = EmailField(label='Email', max_length=100, validators=[profanity_check],
                       widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'john@example.com'}))
    username = CharField(label='Username', min_length=6, max_length=100, validators=[profanity_check],
                      widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'johny_1234'}))
    password = CharField(label='Password', max_length=100, validators=[
        RegexValidator(regex=PASSWORD_PATTERN, message=PASSWORD_MESSAGE)
    ], widget=PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = CharField(label='Confirm password', max_length=100, validators=[
        RegexValidator(regex=PASSWORD_PATTERN, message=PASSWORD_MESSAGE)
    ], widget=PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('Password and confirm password doesn\'t match')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = MongoUser.objects.filter(email=email).first()
        if user:
            raise ValidationError('Is already taken')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = MongoUser.objects.filter(username=username).first()
        if user:
            raise ValidationError('Is already taken')
        return username


class EditProfileForm(Form):
    user_id = CharField(required=False)
    firstname = CharField(label='Firstname', max_length=100, validators=[profanity_check],
                          widget=TextInput(attrs={'class': 'form-control'}))
    lastname = CharField(label='Lastname', max_length=100, validators=[profanity_check],
                         widget=TextInput(attrs={'class': 'form-control'}))
    email = EmailField(label='Email', max_length=100, validators=[profanity_check],
                       widget=TextInput(attrs={'class': 'form-control'}))
    username = CharField(label='Username', min_length=6, max_length=100, validators=[profanity_check],
                      widget=TextInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        check_user = MongoUser.objects.filter(email=self.cleaned_data.get('email')).first()
        user = MongoUser.objects.filter(id=self.cleaned_data.get('user_id')).first()
        if check_user and user.email != self.cleaned_data.get('email'):
            raise ValidationError('is already taken')
        return self.cleaned_data.get('email')

    def clean_username(self):
        check_user = MongoUser.objects.filter(username=self.cleaned_data.get('username')).first()
        user = MongoUser.objects.filter(id=self.cleaned_data.get('user_id')).first()
        if check_user and user.username != self.cleaned_data.get('username'):
            raise ValidationError('is already taken')
        return self.cleaned_data.get('username')


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
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise ValidationError('Password and confirm password doesn\'t match')
