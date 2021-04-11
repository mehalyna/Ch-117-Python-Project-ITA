from typing import Type

from flask import request
from flask_mongoengine import Document
from mongoengine.queryset.visitor import Q

from models import Status, User

ROWS_PER_PAGE = 6


def search_and_pagination(collection: Type[Document], order_field: str, status: str = None):
    search = request.args.get('userSearch')
    page = request.args.get('page', 1, type=int)
    status = [Status.ACTIVE, Status.INACTIVE] if not status else [status]
    if search and collection is User:
        users = collection.objects(
            Q(firstname__contains=search) | Q(lastname__contains=search) | Q(email__contains=search),
            status__in=status).order_by('status', order_field).paginate(page=page, per_page=ROWS_PER_PAGE)
    else:
        users = collection.objects(status__in=status).order_by(
            'status', order_field).paginate(page=page, per_page=ROWS_PER_PAGE)
    return users
