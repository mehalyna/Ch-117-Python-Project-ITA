from typing import Type

from bson import ObjectId
from flask import request
from flask_mongoengine import Document
from mongoengine.queryset.visitor import Q

from models import Author, Book, Status

ROWS_PER_PAGE = 6


def search_and_pagination(collection: Type[Document], order_field: str, status: str = None):
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
    else:
        collection_documents = collection.objects(status__in=status).order_by(
            'status', order_field).paginate(page=page, per_page=ROWS_PER_PAGE)
    return collection_documents
