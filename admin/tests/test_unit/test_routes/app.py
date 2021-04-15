import flask


from admin.tests.test_unit.test_routes.urls import (
    ADMIN_LOGIN, HOME, BOOK_STORAGE
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

    def post_login(self, data: dict, follow_redirects=True) -> flask.Response:
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
