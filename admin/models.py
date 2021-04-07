from datetime import datetime
from flask_login import UserMixin
from mongoengine import DateTimeField, Document, EmailField, EmbeddedDocument, EmbeddedDocumentField, FloatField, \
    IntField, ListField, ReferenceField, StringField
from werkzeug.security import check_password_hash, generate_password_hash


class Status:
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    MUTED = 'muted'


class Role:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class Preference(EmbeddedDocument):
    genres = ListField(default=[])
    authors = ListField(default=[])
    rating = FloatField(default=2.5, min_value=0.0, max_value=5.0)
    years = ListField(default=(), max_length=2)


class User(UserMixin, Document):
    firstname = StringField(max_length=100, min_length=1, required=True)
    lastname = StringField(max_length=100, min_length=1, required=True)
    email = EmailField(required=True, unique=True)
    login = StringField(required=True, unique=True)
    password_hash = StringField(required=True, min_length=8)
    role = StringField(default=Role.USER)
    status = StringField(default=Status.ACTIVE)
    last_login = DateTimeField(default=datetime.now)
    reviews = ListField(default=[])
    recommended_books = ListField(default=[])
    wishlist = ListField(default=[])
    preference = EmbeddedDocumentField(Preference.__name__, default=Preference())

    def __repr__(self):
        return '<Admin {}>'.format(self.login)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

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
        return self.login


class BookStatistic(EmbeddedDocument):
    rating = FloatField(default=2.5, min_value=0.0, max_value=5.0)
    total_read = IntField(default=0, min_value=0)
    reading_now = IntField(default=0, min_value=0)


class Author(Document):
    name = StringField(default='', max_length=500)
    birthdate = StringField(default='', max_length=15)
    death_date = StringField(default='', max_length=15)
    status = StringField(default=Status.ACTIVE, max_length=50)
    books = ListField(default=[])


class Book(Document):
    title = StringField(default='', max_length=200)
    author = StringField(default='Author', max_length=200)
    year = StringField(default='', max_length=20)
    publisher = StringField(default='', max_length=200)
    language = StringField(default='', max_length=20)
    description = StringField(default='', max_length=10000)
    link_img = StringField(default='', max_length=1000)
    pages = IntField(default=1, min_value=1)
    genres = StringField(default='')
    status = StringField(default=Status.ACTIVE, max_length=100)
    store_links = ListField(default=[])
    statistic = EmbeddedDocumentField(BookStatistic.__name__, default=BookStatistic())


class Review(Document):
    user_id = ReferenceField(User.__name__, required=True)
    book_id = ReferenceField(Book.__name__, required=True)
    firstname = StringField(default='', max_length=50)
    lastname = StringField(default='', max_length=50)
    status = StringField(default=Status.ACTIVE, max_length=100)
    comment = StringField(default='', max_length=5000)
    date = DateTimeField(default=datetime.now)
