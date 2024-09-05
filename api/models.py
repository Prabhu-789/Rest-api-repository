from django.core.exceptions import ValidationError
from django.db import models

def validate_only_characters(value):
    if not value.isalpha():
        raise ValidationError(f"{value} contains non-alphabetic characters. Only letters are allowed.")

def validate_only_digits(value):
    if not str(value).isdigit():
        raise ValidationError(f"{value} is not a valid roll number. Only digits are allowed.")

import uuid
from django.db import models

class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100,validators=[validate_only_characters])
    roll = models.IntegerField(validators=[validate_only_digits])
    city = models.CharField(max_length=100,validators=[validate_only_characters])
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # UUID field

    def __str__(self):
        return self.name
