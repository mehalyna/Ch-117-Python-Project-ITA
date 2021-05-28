from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, SelectField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError

from admin.models import Role, Status, MongoUser

EMAIL_PATTERN = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
MIN_PASSWORD_LEN = 8


def unique_check(column: str, update: bool = False):
    message = f'{column.title()} is already taken'

    def _unique_check(form, field):
        user = MongoUser.objects(__raw__={column: field.data}).first()

        if user and update and user.id != form.user_id.data:
            raise ValidationError(message)
        elif user and not update:
            raise ValidationError(message)

    return _unique_check


def update_password_validator(form, field):
    password_len = len(field.data)
    message = f'Field must be at least {MIN_PASSWORD_LEN} character long.'
    if 0 < password_len < MIN_PASSWORD_LEN:
        raise ValidationError(message)


class AddUserForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = EmailField('Email', validators=[
        DataRequired(), Regexp(regex=EMAIL_PATTERN, message='Invalid email'),
        unique_check('email')])
    login = StringField('Login', validators=[DataRequired(), Length(min=6), unique_check('login')])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=MIN_PASSWORD_LEN)
    ])
    role = SelectField('Role', choices=[
        (Role.ADMIN, Role.ADMIN),
        (Role.MODERATOR, Role.MODERATOR),
        (Role.USER, Role.USER)
    ], validators=[DataRequired()])
    submit = SubmitField('Add')


class UpdateUserForm(AddUserForm):
    user_id = StringField('Id')
    email = EmailField('Email', validators=[
        DataRequired(), Regexp(regex=EMAIL_PATTERN, message='Invalid email'),
        unique_check('email', update=True)
    ])
    login = StringField('Login', validators=[
        DataRequired(), unique_check('login', update=True), Length(min=6)
    ])
    password = PasswordField('Password', validators=[
        update_password_validator
    ])
    status = SelectField('Status', choices=[
        (Status.ACTIVE, Status.ACTIVE),
        (Status.INACTIVE, Status.INACTIVE)
    ], validators=[DataRequired()])
    submit = SubmitField('Update')


class LoginForm(FlaskForm):
    admin = StringField('Admin', validators=[DataRequired(), Length(min=6)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=35)])
    submit = SubmitField('Sign In')

    def get_user(self):
        return MongoUser.objects(username=self.admin.data).first()


class AddBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author_name = StringField('Author name', validators=[DataRequired()])
    author_birthdate = IntegerField('Author birthdate', validators=[DataRequired()])
    author_death_date = IntegerField('Author death date', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    img_link = StringField('Image link', validators=[DataRequired()])
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
