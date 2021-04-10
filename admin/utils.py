from flask import request
from mongoengine.queryset.visitor import Q

from models import User

ROWS_PER_PAGE = 6


def search_and_pagination(order_field: str, status: str = None):
    search = request.args.get('searchInput')
    page = request.args.get('page', 1, type=int)
    status = ['active', 'inactive'] if not status else [status]
    if search:
        users = User.objects(
            Q(firstname__contains=search) | Q(lastname__contains=search) | Q(email__contains=search), status__in=status
        ).order_by('status', order_field).paginate(page=page, per_page=ROWS_PER_PAGE)
    else:
        users = User.objects(status__in=status).order_by('status', order_field).paginate(page=page,
                                                                                         per_page=ROWS_PER_PAGE)
    return users
