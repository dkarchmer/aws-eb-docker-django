FROM python:3.4
MAINTAINER David Karchmer <dkarchmer@gmail.com>

# Install PostgreSQL dependencies
RUN apt-get update && apt-get install -y \
            postgresql \
            libpq-dev \
            libjpeg-dev; \
            apt-get clean

RUN pip3 install -U pip

RUN adduser --disabled-password --gecos '' uwsgi

WORKDIR    /var/app

ADD . /var/app/
RUN pip3 install -r requirements.txt

ENV PYTHONPATH /var/app:$PYTHONPATH
#ENV DJANGO_SETTINGS_MODULE=settings.dev-local

EXPOSE 8080

#COPY runserver.sh /var/app/runserver.sh

WORKDIR    /var/app
CMD ["python3", "manage.py", "migrate", "--noinput"]
CMD ["python3", "manage.py", "runserver"]
#ENTRYPOINT ["/var/app/runserver.sh"]

