from werkzeug.security import check_password_hash
from app import db, login
from flask_login import UserMixin


class Admin(UserMixin, db.Document):
    username = db.StringField(max_length=80, unique=True)
    password_hash = db.StringField(max_length=64)

    def __repr__(self):
        return '<Admin {}>'.format(self.username)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __unicode__(self):
        return self.username


# Create user loader function
@login.user_loader
def load_admin(user_id):
    return Admin.objects(id=user_id).first()
