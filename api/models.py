import uuid
from django.db import models
from .validators import validate_only_characters, validate_only_digits  # Make sure this path is correct

class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, validators=[validate_only_characters])
    roll = models.IntegerField(validators=[validate_only_digits])
    city = models.CharField(max_length=100, validators=[validate_only_characters])
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name
