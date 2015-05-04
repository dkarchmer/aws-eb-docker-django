#!/bin/bash

cd /var/app

python3 manage.py migrate --noinput
python3 manage.py runserver