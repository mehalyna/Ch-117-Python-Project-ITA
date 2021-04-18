from admin.tests.config import LOGIN, PASSWORD
from http import HTTPStatus
import io

def test_correct_data(app):
    app.authorize(LOGIN, PASSWORD)
    with open('admin/tests/test_data/books.json', 'rb') as f:
        data = {'file': (io.BytesIO(f.read()), 'books.json')}
    response = app.post_import_file(data)

    assert HTTPStatus.OK == response.status_code
    assert b'All books saved successfully' in response.data

def test_incorrect_data(app):
    app.authorize(LOGIN, PASSWORD)
    with open('admin/tests/test_data/books.json', 'rb') as f:
        data = {'file': (io.BytesIO(f.read(10)), 'books.json')}
    response = app.post_import_file(data)

    assert HTTPStatus.OK == response.status_code
    assert b'Error parsing file:' in response.data

def test_too_large_file(app):
    app.authorize(LOGIN, PASSWORD)
    with open('admin/tests/test_data/books.json', 'rb') as f:
        data = {'file': (io.BytesIO(f.read()*10000), 'books.json')}
    response = app.post_import_file(data)

    assert HTTPStatus.REQUEST_ENTITY_TOO_LARGE == response.status_code
    assert b'The data value transmitted exceeds the capacity limit' in response.data

def test_file_is_not_selected(app):
    app.authorize(LOGIN, PASSWORD)
    data = {'file': (io.BytesIO(b''), '')}
    response = app.post_import_file(data)

    assert HTTPStatus.OK == response.status_code
    assert b'File has not been selected, please choose one' in response.data

def test_wrong_file_type(app):
    app.authorize(LOGIN, PASSWORD)
    with open('admin/tests/test_data/books.json', 'rb') as f:
        data = {'file': (io.BytesIO(f.read()), 'books.png')}
    response = app.post_import_file(data)

    assert HTTPStatus.OK == response.status_code
    assert b'Incorrect type of file (.JSON is needed)' in response.data