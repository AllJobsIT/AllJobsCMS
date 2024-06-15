#!/bin/sh

echo "Run migrations"
python manage.py makemigrations
python manage.py migrate

exec "$@"