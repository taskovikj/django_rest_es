#!/bin/sh

python manage.py makemigrations

# Apply migrations
python manage.py migrate

python manage.py createsuperuser --noinput --username="admin" --email="admin@example.com"
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').update(password='admin')" | python manage.py shell

# Start Django development server
python manage.py runserver 0.0.0.0:8000