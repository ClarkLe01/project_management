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
python manage.py loaddata fixtures/langprogramming.json --app utils.ProgrammingLanguage
python manage.py loaddata fixtures/currencies.json --app utils.Currency
python manage.py loaddata fixtures/users.json --app user.User
python manage.py loaddata fixtures/projects.json --app project.Project
python manage.py loaddata fixtures/files.json --app project.File
python manage.py loaddata fixtures/tasks.json --app project.Task
daphne -b 0.0.0.0 -p 8000 app.asgi:application
exec "$@"


