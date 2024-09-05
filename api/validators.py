from django.core.exceptions import ValidationError

def validate_only_characters(value):
    if not value.isalpha():
        raise ValidationError(f"{value} contains non-alphabetic characters. Only letters are allowed.")

def validate_only_digits(value):
    if not str(value).isdigit():
        raise ValidationError(f"{value} is not a valid roll number. Only digits are allowed.")
