# Generated by Django 5.1 on 2024-09-01 06:01

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('roll', models.IntegerField()),
                ('city', models.CharField(max_length=100)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
    ]
