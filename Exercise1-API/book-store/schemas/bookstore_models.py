from pydantic import BaseModel, field_validator, constr, confloat
import re

class CreateBookRequest(BaseModel):
    title: constr(min_length=1, max_length=300)
    author: constr(min_length=1, max_length=100)
    published_date: str
    isbn: constr(strict=13)
    price: confloat(gt=0)

    @field_validator("published_date")
    def validate_date_format(cls, value):
        # Define the expected date format using a regular expression
        date_format = r"^\d{4}-\d{2}-\d{2}$"

        # Check if the value matches the expected format
        if not value or not bool(re.match(date_format, value)):
            raise ValueError("Date must be in the format 'YYYY-MM-DD'")

        return value