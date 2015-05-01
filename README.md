# README #

This README document an example for how to setup a Docker based Elastic Beanstalk
running a Django Project

## How do I get set up? ##

* install Python 2.7 or Python 3.4
* install git
* install pip
* install virtualenv
* make virtualenv

* pip install -r requirements.txt
* pip install -r local_requirements.txt

### Local Setup ###

* As indicated, you must first install python 2.7/3.4, git, pip and virtualenv
* Using Fabric, you can just do

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

