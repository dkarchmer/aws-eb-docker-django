# README #

This README document an example for how to setup a Docker based Elastic Beanstalk (EB)
running a Django Project with a Postgres RDS instance

This version uses the Generic Docker Platform in EB

## How do I get set up? ##

* install Python 3.4
* install git
* install pip
* install virtualenv
* make virtualenv

* pip install -r requirements.txt
* pip install -r local_requirements.txt

### Local Setup (Fabric) ###

* As indicated, you must first install python 2.7/3.4, git, pip and virtualenv

* fab statics
    * to collect statics
* fab test
    * to run unit tests

* fab migrate
    * To makemigrations and migrate database

* fab runserver
    * To run local server

* fab eb_create
    * To deploy initial setup to AWS Elastic Beanstalk

* fab eb_deploy
    * To deploy code changes to an existing image (previously created)

### Local Setup (Docker compose) ###

Assuming you install docker-compose (https://docs.docker.com/compose/)

* docker-compose up -d
* docker-compose build web // To rebuild django server after changes
* docker-compose run --rm web python manage.py migrate
* docker-compose run --rm web python manage.py initadmin
* docker-compose run --rm web python manage.py test --settings=settings.dev-local

### AWS Elastic Beanstalk Release ###

Assuming credentials stored on ~/.aws/credentials (http://boto.readthedocs.org/en/latest/boto_config_tut.html)

* export AWS_PROFILE='your-profile-name'
* export EB_ENV_NAME='elastic-beanstalk-environment-and-app-name' (we are using env==app names)
* fab eb_create_preconfigured
   * Enter db name and password
   * It can take as much as ten minutes to finish
* After the site is up, go to the following address to initialize the admin account
   * http://<your env>.elasticbeanstalk.com/account/init
   * Then login and change the password

### References ###

* https://realpython.com/blog/python/deploying-a-django-app-to-aws-elastic-beanstalk/