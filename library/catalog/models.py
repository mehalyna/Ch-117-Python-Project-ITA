from copy import copy
from datetime import datetime

from django.contrib.auth import get_user_model
from django_mongoengine import Document
from mongoengine import DateTimeField, EmailField, EmbeddedDocument, EmbeddedDocumentField, FloatField, \
    IntField, ListField, ReferenceField, StringField
from werkzeug.security import check_password_hash, generate_password_hash
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


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


class MongoUser(Document):
    first_name = StringField(max_length=100, min_length=1, required=True)
    last_name = StringField(max_length=100, min_length=1, required=True)
    email = EmailField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True, min_length=8)
    role = StringField(default=Role.USER)
    status = StringField(default=Status.ACTIVE)
    last_login = DateTimeField(default=datetime.now)
    reviews = ListField(default=[])
    recommended_books = ListField(default=[])
    wishlist = ListField(default=[])
    preference = EmbeddedDocumentField(Preference.__name__, default=Preference())

    def generate_passwords(self, password):
        return generate_password_hash(password), make_password(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if self.password:
            self.password, django_password = self.generate_passwords(self.password)
        mongo_user = super().save()
        django_user_model = get_user_model()
        django_user_model.objects.create_user(username=self.username,
                                              email=self.email,
                                              password=django_password)
        return mongo_user

    def update(self, **kwargs):
        mongo_kwargs = copy(kwargs)
        django_kwargs = copy(kwargs)
        if 'password' in kwargs:
            mongo_kwargs['password'], django_kwargs['password'] = \
                self.generate_passwords(kwargs['password'])
        mongo_user = super().update(**mongo_kwargs)

        need_to_update_in_django = ['username', 'password', 'email']
        for field in list(django_kwargs):
            if field not in need_to_update_in_django:
                django_kwargs.pop(field)

        django_user_model = get_user_model()
        django_user_model.objects.filter(username=self.username).update(**django_kwargs)
        return mongo_user

# class CustomManager(UserManager):
#     def _create_user(self, username, email, password, **extra_fields):
#         return super()._create_user(username, email, password, **extra_fields)


class DjangoUser(AbstractUser):
    @property
    def mongo_user(self):
        return MongoUser.objects(username=self.username).first()

    # objects = CustomManager()


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
    statistic = EmbeddedDocumentField(BookStatistic.__name__, default=BookStatistic())


class Review(Document):
    user_id = ReferenceField(MongoUser.__name__, required=True)
    book_id = ReferenceField(Book.__name__, required=True)
    firstname = StringField(default='', max_length=50)
    lastname = StringField(default='', max_length=50)
    status = StringField(default=Status.ACTIVE, max_length=100)
    comment = StringField(default='', max_length=5000)
    rating = IntField(default=0, min_value=0.0, max_value=5)
    date = DateTimeField(default=datetime.now)
