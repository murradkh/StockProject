#!/bin/bash

python manage.py migrate --no-input
echo "no" | python manage.py collectstatic 2>/dev/null
gunicorn --workers=3 myrails.wsgi:application --bind 0.0.0.0:8000
