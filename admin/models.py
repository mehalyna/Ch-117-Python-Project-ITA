from datetime import datetime
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from flask_login import UserMixin
from flask_mongoengine import Document
from mongoengine import (
    DateTimeField, EmailField, FloatField, IntField, ListField, ReferenceField,
    StringField, BooleanField
)


settings.configure()


class Statistics:
    def __init__(self, number_users=0, number_books=0, number_active_users=0, number_inactive_users=0,
                 number_muted_users=0, number_active_books=0, number_inactive_books=0):
        self.number_users = number_users
        self.number_books = number_books
        self.number_active_users = number_active_users
        self.number_inactive_users = number_inactive_users
        self.number_muted_users = number_muted_users
        self.number_active_books = number_active_books
        self.number_inactive_books = number_inactive_books


class Status:
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    MUTED = 'muted'


class Role:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class MongoUser(UserMixin, Document):
    firstname = StringField(max_length=100, min_length=1, required=True)
    lastname = StringField(max_length=100, min_length=1, required=True)
    email = EmailField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True, min_length=8)
    role = StringField(default=Role.USER)
    status = StringField(default=Status.ACTIVE)
    reviews = ListField(default=[])
    recommended_books = ListField(default=[])
    wishlist = ListField(default=[])
    rated_books = ListField(default=[])
    last_login = DateTimeField(default=datetime.now)
    date_joined = DateTimeField(default=datetime.now)
    is_admin = BooleanField(default=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)

    meta = {'collection': 'catalog_mongouser'}

    def __repr__(self):
        return '<Admin {}>'.format(self.username)

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __unicode__(self):
        return self.username


class BookStatistic(Document):
    rating = FloatField(default=2.5, min_value=0.0, max_value=5.0)
    total_read = IntField(default=0, min_value=0)
    reading_now = IntField(default=0, min_value=0)
    stars = ListField(default=[0, 0, 0, 0, 0])

    meta = {'collection': 'catalog_bookstatistic'}


class Author(Document):
    name = StringField(default='', max_length=500)
    birthdate = StringField(default='', max_length=15)
    death_date = StringField(default='', max_length=15)
    status = StringField(default=Status.ACTIVE, max_length=50)
    books = ListField(default=[])

    meta = {'collection': 'catalog_author'}


class Book(Document):
    title = StringField(default='', max_length=200)
    author_id = ReferenceField(Author.__name__)
    year = StringField(default='', max_length=20)
    publisher = StringField(default='', max_length=200)
    language = StringField(default='', max_length=20)
    description = StringField(default='', max_length=10000)
    link_img = StringField(default='', max_length=1000)
    pages = IntField(default=1, min_value=1)
    genres = ListField(default=[])
    status = StringField(default=Status.ACTIVE, max_length=100)
    store_links = ListField(default=[])
    statistic_id = ReferenceField(BookStatistic.__name__)

    meta = {'collection': 'catalog_book'}


class Review(Document):
    user_id = ReferenceField(MongoUser.__name__, required=True)
    book_id = ReferenceField(Book.__name__, required=True)
    firstname = StringField(default='', max_length=50)
    lastname = StringField(default='', max_length=50)
    status = StringField(default=Status.ACTIVE, max_length=100)
    comment = StringField(default='', max_length=5000)
    date = DateTimeField(default=datetime.now)

    meta = {'collection': 'catalog_review'}

