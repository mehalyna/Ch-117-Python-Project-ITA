from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, StringField, SelectField,  SubmitField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields.html5 import EmailField

from models import Role, Status, User


class AddUserForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[
        (Role.ADMIN, Role.ADMIN),
        (Role.MODERATOR, Role.MODERATOR),
        (Role.USER, Role.USER)
    ], validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdateUserForm(AddUserForm):
    status = SelectField('Status', choices=[
        (Status.ACTIVE, Status.ACTIVE),
        (Status.INACTIVE, Status.INACTIVE)
    ], validators=[DataRequired()])


class LoginForm(FlaskForm):
    admin = StringField('Admin', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=35)])
    submit = SubmitField('Sign In')

    def get_user(self):
        return User.objects(admin=self.admin.data).first()

class AddBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    pages = IntegerField('Pages', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    language = StringField('Language', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UpdateBookForm(AddBookForm):
    status = SelectField('Status', choices=[
        (Status.ACTIVE, Status.ACTIVE),
        (Status.INACTIVE, Status.INACTIVE)
    ], validators=[DataRequired()])
