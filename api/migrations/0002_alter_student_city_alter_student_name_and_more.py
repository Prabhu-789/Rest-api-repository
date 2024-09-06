# Generated by Django 5.1 on 2024-09-06 04:23

import api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='city',
            field=models.CharField(max_length=100, validators=[api.validators.validate_only_characters]),
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=100, validators=[api.validators.validate_only_characters]),
        ),
        migrations.AlterField(
            model_name='student',
            name='roll',
            field=models.IntegerField(validators=[api.validators.validate_only_digits]),
        ),
    ]
