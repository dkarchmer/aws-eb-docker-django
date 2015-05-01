__author__ = 'david'

import re
import os, time, json
import requests
from fabric.api import local, env, lcd
from fabric.colors import green as _green, yellow as _yellow
from fabric.colors import red as _red, blue as _blue

import boto
from boto import sqs

AWS_PROFILE='mysite'
R53_DOMAIN_NAME = 'www.mysite.com.'
DOMAIN_NAME = 'https://www.mysite.com'
AWS_REGION = 'us-east-1'


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

def loaddata(app='myproject/fixtures/initial_data.json'):
    # fab loaddata:myproject/fixtures/initial_data.json
    cmd = "./manage.py loaddata %s --settings=settings.dev-local" % app
    local(cmd)

def runserver():
    migrate()
    local("./manage.py runserver --settings=settings.dev-local")

def eb_deploy():
    local("eb deploy --timeout=10")

def eb_create(name='mysite'):

    local('eb init -p python --profile %s %s' % (AWS_PROFILE, name))
    local("eb create -db --timeout=20 --profile %s -c %s %s " % (AWS_PROFILE, name, name))


def setup_route53():
    # Assumes we have a .aws/credentials with the given profile
    r53 = boto.connect_route53(profile_name=AWS_PROFILE)
    elb = boto.connect_elb(profile_name=AWS_PROFILE)

    lb = elb.get_all_load_balancers()[0]#load_balancer_names=elb_name)[0]
    print (_yellow('lb.canonical_hosted_zone_name_id: ') + _green(str(lb.canonical_hosted_zone_name_id )))
    print (_yellow('lb.canonical_hosted_zone_name: ') + _green(str(lb.canonical_hosted_zone_name )))

    zone = r53.get_zone(name='mysite.com.')

    records = zone.get_records()

    for record in records:
        if (record.type == 'A') and (record.name == R53_DOMAIN_NAME):
            print (_yellow("...dropping address record " + _green(record.name) + '(' + _green(record.to_print()) + ') ...'))
            zone.delete_a(record.name)
            time.sleep(1)

    try:
        print (_yellow("...adding address record ALIAS = " + _green(lb.canonical_hosted_zone_name)))
        change = records.add_change("CREATE", R53_DOMAIN_NAME, "A")
        change.set_alias(alias_hosted_zone_id=lb.canonical_hosted_zone_name_id,
                         alias_dns_name= lb.canonical_hosted_zone_name,
                         alias_evaluate_target_health=False)
        result = records.commit()
        change_id = result['ChangeResourceRecordSetsResponse']['ChangeInfo']['Id'].split('/')[-1]
        print (_yellow("...commiting record change " + _green(str(change_id))))

        status = r53.get_change(change_id)['GetChangeResponse']['ChangeInfo']['Status']
        print (_yellow("...status " + _green(str(status))))
        while status != 'INSYNC':
            time.sleep(10)
            status = r53.get_change(change_id)['GetChangeResponse']['ChangeInfo']['Status']
            print (_yellow("...status " + _green(str(status))))
        print(_green('\n[%s]route53 change coalesced' % zone.name))
    except Exception as error:
        if 'already exists' in error.message:
            print (_red('Unable to add www ALIAS'))
            pass
        else:
            raise


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

