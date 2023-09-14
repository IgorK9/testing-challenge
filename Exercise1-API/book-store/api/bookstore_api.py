from flask import Flask, request, jsonify, make_response
from pydantic import ValidationError
from models.bookstore_models import Book

app = Flask(__name__)

# In-memory database
books = []

# Utility function to find a book by ID


def find_book(book_id):
    return next((book for book in books if book['book_id'] == book_id), None)


@app.route('/books', methods=['POST'])
def create_book():
    try:
        data = request.get_json()
        required_fields = ['title', 'author', 'published_date', 'isbn', 'price']
        if not all(field in data for field in required_fields):
            return make_response(
                jsonify({'error': 'Missing required fields'}), 400)
        Book.model_validate(data)
        new_book = {
            'book_id': str(len(books) + 1),
            'title': data['title'],
            'author': data['author'],
            'published_date': data['published_date'],
            'isbn': data['isbn'],
            'price': data['price']
        }

        books.append(new_book)
        return make_response(jsonify(new_book), 201)
    except ValidationError as e:
        return make_response(
            jsonify({'error': f'Data format is wrong: {e.errors()}'}), 400)

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)


@app.route('/books/<string:book_id>', methods=['GET'])
def get_single_book(book_id):
    book = find_book(book_id)
    if book is None:
        return make_response(jsonify({'error': 'Book not found'}), 404)
    return jsonify(book)


@app.route('/books/<string:book_id>', methods=['PUT'])
def update_book(book_id):
    book = find_book(book_id)
    if book is None:
        return make_response(jsonify({'error': 'Book not found'}), 404)

    data = request.get_json()
    for field in ['title', 'author', 'published_date', 'isbn', 'price']:
        if field in data:
            book[field] = data[field]
    return jsonify(book)


@app.route('/books/<string:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = find_book(book_id)
    if book is None:
        return make_response(jsonify({'error': 'Book not found'}), 404)

    books.remove(book)
    return make_response(
        jsonify({'message': 'Book deleted successfully'}), 204)


if __name__ == '__main__':
    app.run(debug=True)
