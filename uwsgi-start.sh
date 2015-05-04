#!/bin/bash

cd /var/app

#. bin/activate

env | grep WSGI
env | grep RDS
env | grep PYTHON
pwd
ls -la

python3 manage.py migrate

# Django support
#WSGI_PATH=/var/app/myproject/wsgi.py
WSGI_PATH=application.py

uwsgi --http :8080 --chdir /var/app --wsgi-file $WSGI_PATH $UWSGI_MODULE --master --processes $UWSGI_NUM_PROCESSES --threads $UWSGI_NUM_THREADS --uid $UWSGI_UID --gid $UWSGI_GID --logto2 $UWSGI_LOG_FILE