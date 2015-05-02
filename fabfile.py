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
    local("./manage.py createsuperuser --username=admin --email=admin@test.com  --settings=settings.dev-local")

def statics():
    local("./manage.py collectstatic --noinput --settings=settings.dev-local")

def migrate():
    local("./manage.py makemigrations --settings=settings.dev-local")
    local("./manage.py migrate --noinput --settings=settings.dev-local")

def test(app=''):
    local('export AWS_PROFILE=%s' % AWS_PROFILE)
    cmd = "./manage.py test %s --settings=settings.dev-local" % app
    local(cmd)

def runserver():
    migrate()
    local("./manage.py runserver --settings=settings.dev-local")

def eb_deploy():
    local("eb deploy --timeout=10")

def eb_create(name=EB_ENV_NAME):

    local('eb init -p docker --profile %s %s' % (AWS_PROFILE, name))
    local("eb create -db --timeout=20 --profile %s -c %s %s " % (AWS_PROFILE, name, name))

def get_db_info():

    rds_conn = boto.connect_rds2(profile_name=AWS_PROFILE)
    if not rds_conn:
        print(_red('Cannot connect to AWS.RDS'))
        return

    instances = rds_conn.describe_db_instances()
    if not instances:
        print(_red('No instances found'))
        return

    inst = instances['DescribeDBInstancesResponse']['DescribeDBInstancesResult']['DBInstances'][0]

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
    print(_blue('db Info ===========>\n'))
    for item in dbinfo:
        print(_green('%20s : %s' % (item, dbinfo[item])))

def post_cmd(api, use_token, data=None, url_name=BASE_URL):

    url = '%s/%s' % (url_name, api)
    if use_token:
        if not authorization_token:
            raise('No Token')
        authorization_str = 'token %s' % authorization_token
        headers = {'content-type': 'application/json',
                   'Authorization': authorization_str}
    else:
        headers = {'Content-Type': 'application/json'}

    if data:
        payload = json.dumps(data)
        r = requests.post(url, data=payload, headers=headers)
    else:
        r = requests.post(url, headers=headers)

    return r

def create_admin(password=ADMIN_INITIAL_PASSWORD, url_name=BASE_URL):
    username = ADMIN_USERNAME
    email = ADMIN_EMAIL
    data = {'username':username,
            'email':email,
            'password':password}
    api = 'api/v1/staff/init/'

    r = post_cmd(api=api, data=data, use_token=False, url_name=url_name)
    if r.status_code == 201:
        print(_green('Admin created'))
    elif r.status_code == 200:
        print(_yellow('Admin was not created: ') + _green('Not Needed'))
    else:
        print(_red('Something wrong: ') + _red(r.content))
