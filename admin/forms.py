from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Regexp, Length, ValidationError
from wtforms.fields.html5 import EmailField

from models import Role, Status, User

EMAIL_PATTERN = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


def unique_check(column):
    message = f'{column.title()} is already taken'

    def _unique_check(form, field):
        if User.objects(__raw__={column: field.data}).first():
            raise ValidationError(message)

    return _unique_check


def update_unique_check(column):
    message = f'{column.title()} is already taken'

    def _update_unique_check(form, field):
        user = User.objects(__raw__={column: field.data}).first()
        if user and user.id != form['user_id'].data:
            raise ValidationError(message)

    return _update_unique_check


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
        DataRequired(), Regexp(regex=EMAIL_PATTERN, message='Invalid email'), update_unique_check('email')])
    login = StringField('Login', validators=[DataRequired(), update_unique_check('login')])
    status = SelectField('Status', choices=[
        (Status.ACTIVE, Status.ACTIVE),
        (Status.INACTIVE, Status.INACTIVE)
    ], validators=[DataRequired()])


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

    def get_user(self):
        return User.objects(admin=self.admin.data).first()
