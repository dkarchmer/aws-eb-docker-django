__author__ = 'david'

import re
import os, time, json
import requests
from fabric.api import local, env, lcd
from fabric.colors import green as _green, yellow as _yellow
from fabric.colors import red as _red, blue as _blue

import boto
from boto import sqs

AWS_PROFILE=os.environ['AWS_PROFILE']
EB_ENV_NAME=os.environ['EB_ENV_NAME']
DOMAIN_NAME = EB_ENV_NAME + '.elasticbeanstalk.com '
BASE_URL = 'http://' + EB_ENV_NAME + '.' + DOMAIN_NAME
AWS_REGION = 'us-east-1'
ADMIN_USERNAME = 'admin'
ADMIN_EMAIL = 'admin@mysite.com'
ADMIN_INITIAL_PASSWORD = 'admin' # To be changed after first login by admin


authorization_token = None

def create_local_admin():
    local("python manage.py createsuperuser --username=admin --email=admin@test.com  --settings=settings.dev-local")

def statics():
    local("python manage.py collectstatic --noinput --settings=settings.dev-local")

def migrate():
    local("python manage.py makemigrations --settings=settings.dev-local")
    local("python manage.py migrate --noinput --settings=settings.dev-local")

def test(app=''):
    local('export AWS_PROFILE=%s' % AWS_PROFILE)
    cmd = "python manage.py test %s --settings=settings.dev-local" % app
    local(cmd)

def runserver():
    migrate()
    local("python manage.py runserver --settings=settings.dev-local")

def eb_deploy():
    local("eb deploy --timeout=10")

def eb_create(name=EB_ENV_NAME):

    local('eb init -p docker --profile %s %s' % (AWS_PROFILE, name))
    local('eb create -db -s --timeout=20 --profile %s -c %s %s ' % (AWS_PROFILE, name, name))

def get_db_info():

    rds_conn = boto.connect_rds2(profile_name=AWS_PROFILE)
    if not rds_conn:
        print(_red('Cannot connect to AWS.RDS'))
        return

    instances = rds_conn.describe_db_instances()
    if not instances:
        print(_red('No instances found'))
        return

    count = len(instances['DescribeDBInstancesResponse']['DescribeDBInstancesResult']['DBInstances'])
    for i in range(0, count):
        inst = instances['DescribeDBInstancesResponse']['DescribeDBInstancesResult']['DBInstances'][i]

        #print(str(inst))

        dbinfo = {}
        endpoint = inst['Endpoint']
        dbinfo['VPCSecurityGroupId'] = inst['VpcSecurityGroups'][0]['VpcSecurityGroupId']
        dbinfo['dbSecurityGroupName'] = inst['DBSecurityGroups'][0]['DBSecurityGroupName']
        dbinfo['host'] = endpoint['Address']
        dbinfo['port'] = endpoint['Port']
        dbinfo['user'] = inst['MasterUsername']
        dbinfo['name'] = inst['DBName']
        dbinfo['instanceClass'] = inst['DBInstanceClass']
        dbinfo['dbID'] = inst['DBInstanceIdentifier']
        dbinfo['Engine'] = inst['Engine']
        dbinfo['EngineVersion'] = inst['EngineVersion']

        print('')
        print(_blue('db Info %d ===========>\n' % i))
        for item in dbinfo:
            print(_green('%20s : %s' % (item, dbinfo[item])))

