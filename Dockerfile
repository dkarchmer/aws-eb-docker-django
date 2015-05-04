FROM python:3.4
MAINTAINER David Karchmer <dkarchmer@gmail.com>

# Install PostgreSQL dependencies
RUN apt-get update && apt-get install -y \
            postgresql \
            libpq-dev \
            libjpeg-dev; \
            apt-get clean

WORKDIR    /var/app

RUN pip3 install virtualenv
RUN virtualenv /var/app
RUN /var/app/bin/pip install --download-cache /src uwsgi

RUN useradd uwsgi -s /bin/false
RUN mkdir /var/log/uwsgi
RUN chown -R uwsgi:uwsgi /var/log/uwsgi

ONBUILD    COPY . /var/app
ONBUILD    RUN /var/app/bin/pip install -r /var/app/requirements.txt

ENV UWSGI_NUM_PROCESSES    1
ENV UWSGI_NUM_THREADS      15
ENV UWSGI_UID              uwsgi
ENV UWSGI_GID              uwsgi
ENV UWSGI_LOG_FILE         /var/log/uwsgi/uwsgi.log

ENV PYTHONPATH $PYTHONPATH:/var/app
ENV DJANGO_SETTINGS_MODULE=settings.production

EXPOSE 8080

COPY uwsgi-start.sh /

CMD        []
ENTRYPOINT ["/uwsgi-start.sh"]

