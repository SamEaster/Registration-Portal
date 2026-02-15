#!/bin/sh
pip install git+https://git@github.com/ping/instagram_private_api.git@1.6.0
python manage.py collectstatic --no-input --clear
#python manage.py createsuperuser --noinput --username alchercaadmin --email alcher@gmail.com
python manage.py migrate
# python manage.py createsuperuser --noinput --firstname admin --email admin@admin.com
gunicorn registrationportal.wsgi:application --bind 0.0.0.0:80 --log-level=debug --timeout 180  --workers 4
