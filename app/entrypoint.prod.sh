#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
python manage.py flush --no-input
python manage.py migrate
daphne -b 0.0.0.0 -p 8000 app.asgi:application
exec "$@"


