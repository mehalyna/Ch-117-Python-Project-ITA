import math
import os
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from djongo import models

CACHE_LIFETIME = int(os.getenv('CACHE_LIFETIME'))

class Status:
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    MUTED = 'muted'


class Role:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class CacheStorage:
    def __init__(self):
        self.__cache_dict = {}


    def get_cache(self, key):
        if key in self.__cache_dict.keys():
            cache = self.__cache_dict[key]
            if cache is None or not cache.is_live():
                self.__cache_dict[key] = None
            else:
                return cache
        return None

    def add_cache(self, key, cache):
        self.__cache_dict[key] = cache

    def clear(self):
        self.__cache_dict = {}

class Cache:
    def __init__(self, data, lifetime=CACHE_LIFETIME):
        ''' value 'lifetime' uses minutes as a unit of measurement '''
        self.data = data
        self.__last_update = datetime.utcnow()
        self.lifetime = lifetime

    def is_live(self):
        return (datetime.utcnow() - self.__last_update).total_seconds()/60 < self.lifetime


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

        user = self.model(
            firstname=firstname,
            lastname=lastname,
            email=self.normalize_email(email),
            username=username,
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

    def update(self, user, firstname, lastname, email, username):
        user.firstname = firstname
        user.lastname = lastname
        user.email = email
        user.username = username
        user.save(using=self._db)


class MongoUser(AbstractBaseUser):
    _id = models.ObjectIdField(primary_key=True)
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


class BookStatistic(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    rating = models.FloatField(default=2.5)
    total_read = models.IntegerField(default=0)
    reading_now = models.IntegerField(default=0)
    stars = models.JSONField(default=[0, 0, 0, 0, 0])


class Author(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(default='', max_length=50)
    birthdate = models.CharField(default='', max_length=15)
    death_date = models.CharField(default='', max_length=15)
    status = models.CharField(default=Status.ACTIVE, max_length=50)
    books = models.JSONField(default=[])


class Book(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    title = models.CharField(default='', max_length=100)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    year = models.CharField(default='', max_length=20)
    publisher = models.CharField(default='', max_length=200)
    language = models.CharField(default='', max_length=20)
    description = models.CharField(default='', max_length=10000)
    link_img = models.CharField(default='', max_length=1000)
    pages = models.IntegerField(default=1)
    genres = models.JSONField(default=[])
    status = models.CharField(default=Status.ACTIVE, max_length=100)
    store_links = models.JSONField(default=[])
    statistic = models.ForeignKey(to=BookStatistic, on_delete=models.CASCADE)

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

        self.statistic.rating = round(rating, 2)
        self.statistic.save()


class Review(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    user = models.ForeignKey(to=MongoUser, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    firstname = models.CharField(default='', max_length=50)
    lastname = models.CharField(default='', max_length=50)
    status = models.CharField(default=Status.ACTIVE, max_length=10)
    comment = models.CharField(default='', max_length=5000)
    date = models.DateTimeField(auto_now=True)
