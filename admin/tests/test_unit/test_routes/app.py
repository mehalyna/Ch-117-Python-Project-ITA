import json

import flask

from admin.tests.test_unit.test_routes.urls import (
    ADMIN_LOGIN, BOOK_STORAGE, CREATE_USER, HOME
)


class App:
    def __init__(self, client):
        self.client = client

    def authorize(self, login: str, password: str) -> flask.Response:
        response = self.post_login(data={'admin': login, 'password': password})
        return response

    def get_login(self) -> flask.Response:
        response = self.client.get(ADMIN_LOGIN)
        return response

    def post_login(self, data: dict, follow_redirects: bool = True) -> flask.Response:
        response = self.client.post(ADMIN_LOGIN,
                                    data=data,
                                    follow_redirects=follow_redirects)
        return response

    def get_home(self) -> flask.Response:
        response = self.client.get(HOME)
        return response

    def get_book_storage(self, params: dict = None) -> flask.Response:
        response = self.client.get(BOOK_STORAGE, query_string=params)
        return response

    def get_user_create(self) -> flask.Response:
        response = self.client.get(CREATE_USER)
        return response

    def post_user_create(self, data: dict, follow_redirects: bool = True) -> flask.Response:
        response = self.client.post(CREATE_USER, data=data, follow_redirects=follow_redirects)

        return response
