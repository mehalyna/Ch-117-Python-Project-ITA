from datetime import datetime
from django_mongoengine import Document
from mongoengine import DateTimeField, EmailField, EmbeddedDocument, EmbeddedDocumentField, FloatField, \
    IntField, ListField, ReferenceField, StringField
from werkzeug.security import check_password_hash, generate_password_hash
from django.contrib.auth.models import User
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

    def set_password(self, password):
        self.django_password = make_password(password)
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        mongo_user = super().save()
        django_user = User(username=self.login, email=self.email, password=self.django_password)
        django_user.save()
        return mongo_user

    def update(self, **kwargs):
        mongo_user = super().update(**kwargs)
        User.objects.filter(username=self.login).update(**kwargs)
        return mongo_user

# class CustomManager(UserManager):
#     def _create_user(self, username, email, password, **extra_fields):
#         return super()._create_user(username, email, password, **extra_fields)


# class DjangoUser(AbstractUser):
#     def get_mongo_user(self):
#         pass
#
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         mu = MongoUser(username=self.username, email=self.email)
#         mu.set_password(self.password)
#         mu.save()

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
