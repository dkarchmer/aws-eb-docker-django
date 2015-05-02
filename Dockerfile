
FROM python:3.4
MAINTAINER David Karchmer <dkarchmer@ampervue.com>

# create unprivileged user
RUN adduser --disabled-password --gecos '' myuser

# Install PostgreSQL dependencies
# Install Postgres
RUN apt-get update && apt-get install -y \
            postgresql-9.3 \
            libpq-dev \
            libjpeg-dev; \
            apt-get clean

# Step 1: Install any Python packages
# ----------------------------------------

RUN mkdir /var/app
WORKDIR  /var/app
COPY requirements.txt /var/app/
RUN pip install -r requirements.txt

# Step 2: Copy Django Code
# ----------------------------------------

COPY authentication /var/app/authentication
COPY myproject /var/app/myproject
COPY settings /var/app/settings
COPY manage.py /var/app/

ENV DJANGO_SETTINGS_MODULE=settings.production
#ENV RDS_DB_NAME=ebdb
#ENV RDS_USERNAME=ebroot

#ENV RDS_PORT=5432

# Useless as there is no port really exposed but seems like EB needs it
EXPOSE 8080

VOLUME ["/var/log/vps"]
VOLUME ["/var/app"]

CMD ["python3", "manage.py", "migrate", "--noinput"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]
