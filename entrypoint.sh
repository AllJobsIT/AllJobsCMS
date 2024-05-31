#!/bin/sh

echo "Run migrations"
python manage.py migrate
python manage.py update_translation_fields

exec "$@"