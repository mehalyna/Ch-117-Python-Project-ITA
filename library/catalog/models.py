import math
from copy import copy
from datetime import datetime

from django.contrib.auth import get_user_model
from django_mongoengine import Document
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django_mongoengine.forms.fields import DictField
from mongoengine import DateTimeField, EmailField, EmbeddedDocument, EmbeddedDocumentField, FloatField, \
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
    # rated_books = DictField(default={})
    preference = EmbeddedDocumentField(Preference.__name__, default=Preference())

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if self.password:
            User = get_user_model()
            User.objects.create_user(username=self.username,
                                     email=self.email,
                                     password=self.password)

            self.password = generate_password_hash(self.password)
        mongo_user = super().save()
        return mongo_user

    def update(self, **kwargs):
        mongo_kwargs = copy(kwargs)
        django_kwargs = copy(kwargs)
        if 'password' in kwargs:
            mongo_kwargs['password'] = generate_password_hash(kwargs['password'])
            django_kwargs['password'] = make_password(kwargs['password'])
            
        mongo_user = super().update(**mongo_kwargs)

        need_to_update_in_django = ['username', 'password', 'email']
        for field in list(django_kwargs):
            if field not in need_to_update_in_django:
                django_kwargs.pop(field)

        django_user_model = get_user_model()
        django_user_model.objects.filter(username=self.username).update(**django_kwargs)
        return mongo_user


class DjangoUser(AbstractUser):
    @property
    def mongo_user(self):
        return MongoUser.objects(username=self.username).first()


class BookStatistic(EmbeddedDocument):
    rating = FloatField(default=2.5, min_value=0.0, max_value=5.0)
    total_read = IntField(default=0, min_value=0)
    reading_now = IntField(default=0, min_value=0)
    stars = ListField(default=[0, 0, 0, 0, 0])


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

    def calculate_rating(self):
        """
        The expression is the lower bound of a normal approximation to a Bayesian credible interval
        for the average rating
        http://www.evanmiller.org/ranking-items-with-star-ratings.html

        """
        number_of_vote = sum(self.statistic.stars)
        number_of_stars = len(self.statistic.stars)
        stars_by_value = list(range(number_of_stars, 0, -1))
        price_stars = [star_value ** 2 for star_value in stars_by_value]

        # Z is the 1−α/2 (α=0.1) quantile of a normal distribution, constant in that case
        Z = 1.65

        def get_sum_from_expression(stars_by_value, stars):
            number_of_vote = sum(stars)
            number_of_stars = len(stars)
            return sum(star_value * (number_of_vote_for_every_star + 1) for star_value, number_of_vote_for_every_star in
                       zip(stars_by_value, stars)) / (number_of_vote + number_of_stars)

        result_sum = get_sum_from_expression(stars_by_value, self.statistic.stars)
        rating = result_sum - Z * math.sqrt(
            (get_sum_from_expression(price_stars, self.statistic.stars) - result_sum ** 2) / (
                        number_of_vote + number_of_stars + 1))

        super(Book, self).update(statistic__rating=round(rating, 2))


class Review(Document):
    user_id = ReferenceField(MongoUser.__name__, required=True)
    book_id = ReferenceField(Book.__name__, required=True)
    firstname = StringField(default='', max_length=50)
    lastname = StringField(default='', max_length=50)
    status = StringField(default=Status.ACTIVE, max_length=100)
    comment = StringField(default='', max_length=5000)
    rating = IntField(default=0, min_value=0.0, max_value=5)
    date = DateTimeField(default=datetime.now)
