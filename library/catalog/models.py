import math
from datetime import datetime

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from djongo import models
from django_mongoengine import Document
from mongoengine import DateTimeField, EmbeddedDocument, EmbeddedDocumentField, FloatField, \
    IntField, ListField, ReferenceField, StringField


class Status:
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    MUTED = 'muted'


class Role:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class Preference(models.Model):
    id = models.AutoField(primary_key=True)
    genres = models.JSONField(default=[])
    authors = models.JSONField(default=[])
    rating = models.FloatField(default=2.5)
    years = models.JSONField(default=[], max_length=2)


class CustomUserManager(BaseUserManager):
    def create_user(self, firstname, lastname, email, username, password=None):
        if not firstname:
            raise ValueError('Users must have a firstname')
        if not lastname:
            raise ValueError('Users must have a lastname')
        if not email:
            raise ValueError('Users must have an email')
        if not username:
            raise ValueError('Users must have an username')
        if not password:
            raise ValueError('Users must have a password')

        preference = Preference()
        preference.save()
        user = self.model(
            firstname=firstname,
            lastname=lastname,
            email=self.normalize_email(email),
            username=username,
            preference=preference
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, firstname, lastname, email, username, password=None):
        user = self.create_user(
            firstname=firstname,
            lastname=lastname,
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.role = Role.ADMIN
        user.save(using=self._db)
        return user


class MongoUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(default=Role.USER, max_length=10)
    status = models.CharField(default=Status.ACTIVE, max_length=10)
    reviews = models.JSONField(default=[])
    recommended_books = models.JSONField(default=[])
    wishlist = models.JSONField(default=[])
    rated_books = models.JSONField(default={})
    preference = models.ForeignKey(to=Preference, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'email', 'password']

    def __str__(self):
        return self.username


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
    date = DateTimeField(default=datetime.now)
