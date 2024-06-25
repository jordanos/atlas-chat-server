#!/bin/sh
cd server

migrate() {
    python manage.py makemigrations
    python manage.py migrate
}

start_server() {
    if [ "$DEBUG" = "True" ]
    then
        echo "Starting development server"
        python manage.py runserver 0.0.0.0:8000
    else
        echo "Starting production server"
        daphne -p 8000 -b 0.0.0.0 config.asgi:application
    fi
}


if [ "$MAKE_MIGRATIONS" = "True" ]
then
    migrate
fi

start_server