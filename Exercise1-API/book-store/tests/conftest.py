import pytest
from api.bookstore_api import app, books

@pytest.fixture(scope="module")
def flask_app():
    """
    Returns flask app instance
    """
    yield app

@pytest.fixture(scope="module")
def client(flask_app):
    """
    Returns flask client
    """
    yield app.test_client()

@pytest.fixture(scope="function", autouse=True)
def books_database():
    """
    Returns a books database
    Empty the database on teardown
    """
    yield books
    books.clear()

@pytest.fixture(scope="module")
def book():
    """
    Return a book
    """
    book = {
        'title': 'Test book',
        'author': 'Bob White',
        'published_date': '2023-01-01',
        'isbn': '1234567890123',
        'price': 12.95
    }
    yield book

@pytest.fixture(scope="module")
def book_modified():
    """
    Return a book
    """
    book = {
        'title': 'Test book 1',
        'author': 'Bob Smith',
        'published_date': '2023-02-02',
        'isbn': '1234567890123',
        'price': 12.95
    }
    yield book

@pytest.fixture(scope="module")
def book_missing_data():
    """
    Return a book
    """
    book = {
        'title': 'Test book',
        'author': 'Bob White'
    }
    yield book

@pytest.fixture(scope="module")
def book_wrong_data_format():
    """
    Return a book
    """
    book = {
        'title': 100,
        'author': '',
        'published_date': '2023-01',
        'isbn': '123',
        'price': '12'
    }
    yield book