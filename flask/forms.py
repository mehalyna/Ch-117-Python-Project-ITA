from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField


class AddUserForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user')
    ], validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdateUserForm(AddUserForm):
    status = SelectField('Status', choices=[
            ('active', 'active'),
            ('inactive', 'inactive')
        ], validators=[DataRequired()])
