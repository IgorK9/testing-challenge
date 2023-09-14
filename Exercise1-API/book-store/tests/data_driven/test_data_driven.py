import json
import pytest
from os import path

def read_data_from_json(file):
    file_path = path.relpath(file)
    with open(file_path) as f:
        data = json.load(f)
    data = [(obj['data'], obj['expected']) for obj in data]
    return data

@pytest.mark.parametrize('input,expected', read_data_from_json('tests/test_data/books.json'))
def test_create_book_correct_data(client, input, expected):
    """
    GIVEN Book data is provided
    WHEN User creates a new book
    THEN Response code matches expected one
    """
    book = input
    code = expected['code']
    response = client.post('/books', json=book)
    assert response.status_code == code