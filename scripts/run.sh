#!/bin/sh


set -e

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4