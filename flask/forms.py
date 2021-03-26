from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import DataRequired


class AddUserForm(FlaskForm):
    firstname = StringField('Firstname')
    lastname = StringField('Lastname')
    email = StringField('Email')
    password = PasswordField('Password')
    role = SelectField('Role', choices=[
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user')
    ])


class UpdateUserForm(FlaskForm):
    firstname = StringField('Firstname')
    lastname = StringField('Lastname')
    email = StringField('Email')
    password = PasswordField('Password')
    role = SelectField('Role', choices=[
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user')
    ])
    status = SelectField('Status', choices=[
        ('active', 'active'),
        ('inactive', 'inactive')
    ])

