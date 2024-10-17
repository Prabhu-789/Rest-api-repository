#!/bin/sh

while ! nc -z $DB_HOST $DB_PORT; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

python manage.py migrate

python manage.py collectstatic --noinput

exec "$@"
