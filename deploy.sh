#!/bin/bash

ps -ef | grep -i manage.py | awk '{print $2}' | xargs kill
git pull
pip install -r requirements.txt
openssl rsautl -decrypt -inkey $PATH_TO_PRIVATE_KEY_PEM -in myrails/configuration/prod.encrypted -out myrails/configuration/prod.cfg
python manage.py migrate
nohup /opt/bitnami/python/bin/python manage.py runserver 0.0.0.0:8000 &