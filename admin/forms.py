from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, SelectField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError

from models import Role, Status, User

EMAIL_PATTERN = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


def unique_check(column, update=False):
    message = f'{column.title()} is already taken'

    def _unique_check(form, field):
        user = User.objects(__raw__={column: field.data}).first()

        if user and update and user.id != form.user_id.data:
            raise ValidationError(message)
        elif user and not update:
            raise ValidationError(message)

    return _unique_check


class AddUserForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = EmailField('Email', validators=[
        DataRequired(), Regexp(regex=EMAIL_PATTERN, message='Invalid email'),
        unique_check('email')])
    login = StringField('Login', validators=[DataRequired(), unique_check('login')])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=8, message='Password should be at least 8 symbols in length')
    ])
    role = SelectField('Role', choices=[
        (Role.ADMIN, Role.ADMIN),
        (Role.MODERATOR, Role.MODERATOR),
        (Role.USER, Role.USER)
    ], validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdateUserForm(AddUserForm):
    user_id = StringField('Id')
    email = EmailField('Email', validators=[
        DataRequired(), Regexp(regex=EMAIL_PATTERN, message='Invalid email'),
        unique_check('email', update=True)
    ])
    login = StringField('Login', validators=[
        DataRequired(), unique_check('login', update=True)
    ])
    status = SelectField('Status', choices=[
        (Status.ACTIVE, Status.ACTIVE),
        (Status.INACTIVE, Status.INACTIVE)
    ], validators=[DataRequired()])


class LoginForm(FlaskForm):
    admin = StringField('Admin', validators=[DataRequired(), Length(min=6)])
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
