from enum import Enum

class ApiErrors(str, Enum):
    wrongDataFormat = 'Data format is wrong'
    missingRequiredFields = 'Missing required fields'
    bookNotFound = 'Book not found'

class ModelsErrors(Enum):
    wrongDataFormat = 'Date must be in the format "YYYY-MM-DD"'