import re
from typing import Type

from bson import ObjectId
from flask import request
from flask_mongoengine import Document
from mongoengine.queryset.visitor import Q

from models import Author, Book, Status, User

ROWS_PER_PAGE = 6


def search_and_pagination(collection: Type[Document], order_field: str, status: str = None):
    user_search = request.args.get('userSearch')
    book_search = request.args.get('bookSearch')
    page = request.args.get('page', 1, type=int)
    status = [Status.ACTIVE, Status.INACTIVE] if not status else [status]
    if book_search and collection is Book:
        collection_documents = collection.objects(
            Q(title__contains=book_search) | Q(year__contains=book_search), status__in=status
        ).order_by('status', 'title').paginate(page=page, per_page=ROWS_PER_PAGE)

        author = Author.objects(name__contains=book_search).first()
        if author:
            arr = []
            for i in author.books:
                author_books_search = Book.objects(id=ObjectId(i)).first()
                if author_books_search:
                    arr.append(author_books_search)
            collection_documents.items += arr
    elif user_search and collection is User:
        collection_documents = collection.objects(
            Q(firstname__contains=user_search) | Q(lastname__contains=user_search) | Q(email__contains=user_search),
            status__in=status).order_by('status', order_field).paginate(page=page, per_page=ROWS_PER_PAGE)
    else:
        collection_documents = collection.objects(status__in=status).order_by(
            'status', order_field).paginate(page=page, per_page=ROWS_PER_PAGE)
    return collection_documents


def back_to_page(page_name: str, search_name: str, prev_url_name: str = None):
    prev_url = request.args.get(prev_url_name)
    if not prev_url:
        final_url = '/users_list' if 'user' in re.split(r'[-_/]', request.path) else 'book-storage'
        return final_url
    else:
        search = request.args.get(search_name)
        page = request.args.get(page_name, 1, type=int)
        params_dict = {search_name: search, page_name: page}
        final_url = f'{prev_url}?'
        for param_name, param_value in params_dict.items():
            if param_name and param_value:
                final_url += f'&{param_name}={param_value}'

        return final_url
