FROM python:3.4

MAINTAINER David Karchmer <dkarchmer@gmail.com>

ENV C_FORCE_ROOT 1

# create unprivileged user
RUN adduser --disabled-password --gecos '' myuser

# Install PostgreSQL dependencies
RUN apt-get update && \
    apt-get install -y postgresql-client libpq-dev && \
    rm -rf /var/lib/apt/lists/*


# Step 1: Install any Python packages
# ----------------------------------------

ENV PYTHONUNBUFFERED 1
RUN mkdir /var/app
WORKDIR  /var/app
COPY requirements.txt /var/app/requirements.txt
RUN pip install -r requirements.txt

# Step 2: Copy Django Code
# ----------------------------------------

COPY . /var/app/.

EXPOSE 8080

CMD ["/var/app/runserver.sh"]

