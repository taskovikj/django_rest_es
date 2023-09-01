#!/bin/sh

python manage.py makemigrations

# Apply migrations
python manage.py migrate


# Start Django development server
python manage.py runserver 0.0.0.0:8000

#Load database
python manage.py loaddata dump.json