#!/bin/bash



# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Run the Django server
exec "$@"

 