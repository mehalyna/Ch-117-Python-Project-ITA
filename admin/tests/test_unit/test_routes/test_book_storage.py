from http import HTTPStatus


from admin.tests.config import LOGIN, PASSWORD


def test_get_book_storage(app):
    app.authorize(LOGIN, PASSWORD)
    response = app.get_book_storage()

    assert HTTPStatus.OK == response.status_code
    assert b'Title' in response.data
    assert b'Author' in response.data
    assert b'Showing page 0' in response.data


def test_get_second_page_in_book_storage(app):
    app.authorize(LOGIN, PASSWORD)
    response = app.get_book_storage({'page': 2})
    assert HTTPStatus.OK == response.status_code
    assert b'Page not found' in response.data
