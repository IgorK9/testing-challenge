import tests.support.error_messages as errMsgs

def test_get_books_database_empty(client):
    """
    GIVEN Books database is empty
    WHEN User retrieves a list of all books
    THEN Response code is 200 and response is empty
    """
    response = client.get('/books')
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_books_database_not_empty(client, book, books_database):
    """
    GIVEN One book is added to the books database
    WHEN User retrieves a list of all books
    THEN Response code is 200 and database contains 1 book
    """
    id = '1'
    book['book_id'] = id
    books_database.append(book)
    response = client.get('/books')
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_create_book_correct_data(client, book, books_database):
    """
    GIVEN Book data is correct
    WHEN User creates a new book
    THEN Response code is 201, new book data matches the original
    and book id is assigned
    """
    response = client.post('/books', json=book)
    new_book = response.get_json()
    assert response.status_code == 201
    assert set(book.items()).issubset(set(new_book.items()))
    assert new_book['book_id']
    assert len(books_database) == 1
    assert set(book.items()).issubset(set(books_database[0].items()))

def test_create_book_missing_data(client, book_missing_data, books_database):
    """
    GIVEN Some of the required keys are missing in a book json
    WHEN User creates a new book
    THEN Response code is 400 and error message
    'Missing required fields' is displayed
    """
    response = client.post('/books', json=book_missing_data)
    assert response.status_code == 400
    assert response.get_json()['error'] == errMsgs.ApiErrors.missingRequiredFields
    assert len(books_database) == 0

def test_create_book_wrong_data_format(client, book_wrong_data_format, books_database):
    """
    GIVEN Data format of strings is not matching json schema
    WHEN User creates a new book
    THEN Response code is 400 and error message
    'Data format is wrong: <error>' is displayed
    """
    response = client.post('/books', json=book_wrong_data_format)
    assert response.status_code == 400
    assert errMsgs.ApiErrors.wrongDataFormat in response.get_json()['error']
    assert len(books_database) == 0

def test_create_book_author_below_min_charachters(client, book, books_database):
    """
    GIVEN Data format of strings is not matching json schema
    WHEN User creates a new book with author name below min charachters
    THEN Response code is 400 and error message
    'Data format is wrong: <error>' is displayed
    """
    book['author'] = ''
    response = client.post('/books', json=book)
    assert response.status_code == 400
    assert errMsgs.ApiErrors.wrongDataFormat in response.get_json()['error']
    assert len(books_database) == 0

def test_create_book_author_exceeding_max_charachters(client, book, books_database):
    """
    GIVEN Data format of strings is not matching json schema
    WHEN User creates a new book with more charachters than allowed
    THEN Response code is 400 and error message
    'Data format is wrong: <error>' is displayed
    """
    book['author'] = 'a'*110
    response = client.post('/books', json=book)
    assert response.status_code == 400
    assert errMsgs.ApiErrors.wrongDataFormat in response.get_json()['error']
    assert len(books_database) == 0

def test_get_books_get_single_book(client, book, books_database):
    """
    GIVEN One book is added to the database
    WHEN User retrieves a single book by id
    THEN Response code is 200 and retrieved book
    data is equal to the one created before
    """
    id = '1'
    book['book_id'] = id
    books_database.append(book)
    response = client.get(f'/books/{id}')
    assert response.status_code == 200
    assert set(book.items()).issubset(set(response.get_json().items()))

def test_get_books_get_single_book_no_book_found(client):
    """
    GIVEN Books database is empty
    WHEN User retrieves a single book by id
    THEN Response code is 404 and error message is
    'Book not found'
    """
    id = 1
    response = client.get(f'/books/{id}')
    assert response.status_code == 404
    assert response.get_json()['error'] == errMsgs.ApiErrors.bookNotFound

def test_update_book(client, book, book_modified, books_database):
    """
    GIVEN Book is added to the database
    WHEN User updates the book by a valid id
    THEN Response code is 200 and the book is updated
    """
    id = '1'
    book['book_id'] = id
    books_database.append(book)
    response = client.put(f'/books/{id}', json=book_modified)
    assert response.status_code == 200
    book_put_response = response.get_json()
    assert set(book_modified.items()).issubset(set(book_put_response.items()))
    assert set(book_modified.items()).issubset(set(books_database[0].items()))

def test_update_book_no_book_found(client, book, book_modified, books_database):
    """
    GIVEN Book is added to the database
    WHEN User updates the book by an invalid id
    THEN Response code is 404 and error message is
    'Book not found'
    """
    id = 2
    book['book_id'] = '1'
    books_database.append(book)
    response = client.put(f'/books/{id}', json=book_modified)
    assert response.status_code == 404
    assert response.get_json()['error'] == errMsgs.ApiErrors.bookNotFound

def test_delete_book(client, book, books_database):
    """
    GIVEN Book is added to the database
    WHEN User deletes the book by a valid id
    THEN Response code is 204 and the book is deleted
    """
    id = '1'
    book['book_id'] = id
    books_database.append(book)
    response = client.delete(f'/books/{id}')
    assert response.status_code == 204
    assert len(books_database) == 0

def test_delete_book_not_found(client, book, books_database):
    """
    GIVEN Book is added to the database
    WHEN User deletes the book by an invalid id
    THEN Response code is 404 and error message is
    'Book not found'
    """
    id = 2
    book['book_id'] = '1'
    books_database.append(book)
    response = client.delete(f'/books/{id}')
    assert response.status_code == 404
    assert len(books_database) == 1

# data driven tests