#!/bin/bash

pkill python
git pull
pip install -r requirements.txt
openssl rsautl -decrypt -inkey $PATH_TO_PRIVATE_KEY_PEM -in myrails/configuration/prod.encrypted -out myrails/configuration/prod.cfg
python manage.py migrate
nohup python manage.py runserver 0.0.0.0:8000 &
