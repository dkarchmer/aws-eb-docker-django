# Use the AWS Elastic Beanstalk Python 3.4 image
FROM amazon/aws-eb-python:3.4.2-onbuild-3.5.1
MAINTAINER David Karchmer <dkarchmer@gamail.com>

# Exposes port 8080
EXPOSE 8080

# Install PostgreSQL dependencies
RUN apt-get update && \
    apt-get install -y postgresql libpq-dev && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH $PYTHONPATH:/var/app
ENV DJANGO_SETTINGS_MODULE=settings.production