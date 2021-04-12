from typing import Type
import re

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


def back_to_page(page_name: str, search_name: str, prev_url_name: str = None):
    prev_url = request.args.get(prev_url_name)
    if not prev_url:
        final_url = '/users_list' if 'user' in re.split(r'[-_/]', request.path) else 'book-storage'
        return final_url
    else:
        search = request.args.get(search_name, '')
        page = request.args.get(page_name, 1, type=int)
        params_dict = {search_name: search, page_name: page}
        final_url = f'{prev_url}?'
        for param_name, param_value in params_dict.items():
            final_url += f'&{param_name}={param_value}'

        return final_url
