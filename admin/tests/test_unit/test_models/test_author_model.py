import pytest
from mongoengine.errors import ValidationError
from flask_mongoengine import BaseQuerySet

from admin.models import Author


def test_author_model(client):
    author = Author(name='author', birthdate='1993')
    author.save()

    db_author = Author.objects(name='author').first()
    assert 'author' == db_author.name
    db_author.delete()


def test_author_save_with_invalid_name(client):
    with pytest.raises(ValidationError) as exception:
        author = Author(name=1)
        author.save()
        author.delete()
    assert 'StringField only accepts string values' in exception.value.message


def test_get_not_existing_author(client):
    author = Author.objects(name='some not existing author')
    # If author is in db it will be instance of Author class
    assert isinstance(author, BaseQuerySet)


def test_get_author_by_not_existing_attribute(client):
    author = Author.objects(gander='male')
    # If author is in db it will be instance of Author class
    assert isinstance(author, BaseQuerySet)
