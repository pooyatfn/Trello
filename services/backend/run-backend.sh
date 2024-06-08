#!/bin/bash

if [ "$DEVELOPMENT_ENVIRONMENT" == "development" ]
then
    echo "make migrations"
    python manage.py makemigrations
fi


echo "migrate db for start backend"
python manage.py migrate


if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL"
fi


echo "Running backend"
if [ "$APPLICATION_SERVER" == "runserver" ]
then
    echo "runserver 0.0.0.0:8000"
    python manage.py runserver 0.0.0.0:8000
else
    WORKERS_COUNT=$(cat /proc/cpuinfo | awk '/^processor/{print $3}' | wc -l)
    echo "gunicorn 0.0.0.0:8000"
    python -m gunicorn \
        --access-logfile /var/log/backend/access.log \
        --error-logfile /var/log/backend/error.log \
        --timeout 500 \
        --capture-output \
        --log-level debug \
        --workers "$WORKERS_COUNT" \
        --bind 0.0.0.0:8000 \
        backend.wsgi:application
fi
