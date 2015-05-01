#import unittest
from django.test import TestCase, Client
from django.core import mail
import json

from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from myproject.main.models import *

from django.contrib.auth import get_user_model
user_model = get_user_model()

class MainTestCase(TestCase):
    """
    Fixure includes:
    """
    #fixtures = ['testdb_main.json']

    def setUp(self):
        self.u1 = user_model.objects.create_superuser(username='user1', email='user1@foo.com', password='pass')
        self.u1.is_active = True
        self.u1.save()
        self.u2 = user_model.objects.create_user(username='user2', email='user2@foo.com', password='pass')
        self.u2.is_active = True
        self.u2.save()
        self.u3 = user_model.objects.create_user(username='user3', email='user3@foo.com', password='pass')
        self.u3.is_active = True
        self.u3.save()
        return

    def tearDown(self):
        user_model.objects.all().delete()

    def testPages(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/about')
        self.failUnlessEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/robots.txt')
        self.failUnlessEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.login(username='user1', password='pass')
        response = self.client.get('/', {})
        self.failUnlessEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

