from datetime import datetime
from django_mongoengine import Document, EmbeddedDocument
from mongoengine import DateTimeField, EmbeddedDocumentField, EmailField, FloatField, ListField, StringField


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


class User(Document):
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
