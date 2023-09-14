# Book Store REST API

## Requirements

Install with poetry:

```shell script
poetry shell
poetry install 
```

## How to run the API

```bash
python bookstore_api.py

```

Your API will start running at **`http://127.0.0.1:5000/`**.

## Run Tests

Tests are located in book-store/tests

Tests are organized in the following way:
Functional tests and boundary tests: book-store/tests/functional
Unit tests (models testing from book-store/models): book-store/tests/unit
Data driven tests: book-store/tests/data_driven
Test data (e.g. for data driven tests): book-store/tests/test_data
Support/helpers (e.g. test error messages enums): book-store/tests/support


To run tests make sure you created a venv under the project directory (book-store)

Install necessary requirements
```bash
pip install -r requirements.txt

```

Run pytest
```bash
pytest

```

To run certain type of tests separetely you specify the file containing tests
```bash
pytest tests/data_driven/test_data_driven.py

```
