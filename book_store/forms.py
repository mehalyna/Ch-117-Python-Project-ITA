from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from models import Admin


class LoginForm(FlaskForm):
    admin = StringField('Admin', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

    def get_user(self):
        return Admin.objects(admin=self.admin.data).first()
