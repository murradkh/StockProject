#!/bin/bash

pkill python
git pull
pip install -r requirements.txt
python manage.py migrate
nohup python manage.py runserver 0.0.0.0:8000 &
