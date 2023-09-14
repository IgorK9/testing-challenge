import pytest
from models.bookstore_models import Book
from pydantic import ValidationError

def test_validate_book_correct_data(book):
    test_book = Book(
        title=book['title'],
        author=book['author'],
        published_date=book['published_date'],
        isbn=book['isbn'],
        price=book['price']
    )
    assert test_book.title == book['title']
    assert test_book.author == book['author']
    assert test_book.published_date == book['published_date']
    assert test_book.isbn == book['isbn']
    assert test_book.price == book['price']

def test_validate_book_missing_data(book):
    with pytest.raises(ValidationError):
        Book(
            title=book['title'],
            author=book['author'],
            published_date=book['published_date'],
            isbn=book['isbn']
        )

def test_validate_book_wrong_data_format(book):
    with pytest.raises(ValueError):
        Book(
            title=book['title'],
            author=book['author'],
            published_date='14 September 2023',
            isbn=book['isbn'],
            price=book['price']
        )

# TODO cover all scenarios + description