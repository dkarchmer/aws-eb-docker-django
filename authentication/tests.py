from django.test import TestCase, Client
from django.core import mail
import json

from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework import status

from authentication.models import *
from authentication.serializers import AccountSerializer

from django.contrib.auth import get_user_model
user_model = get_user_model()

class MainTestCase(TestCase):
    """
    Fixure includes:
    """
    #fixtures = ['testdb_main.json']

    def setUp(self):
        self.u1 = user_model.objects.create_superuser(username='user1', email='user1@foo.com', password='pass')
        self.u1.name = 'User One'
        self.u1.is_active = True;
        self.u1.save()
        self.u2 = user_model.objects.create_user(username='user2', email='user2@foo.com', password='pass')
        self.u2.name = 'User G Two'
        self.u2.save()
        self.u3 = user_model.objects.create_user(username='user3', email='user3@foo.com', password='pass')
        self.token1 = Token.objects.create(user=self.u1)
        self.token2 = Token.objects.create(user=self.u2)

    def tearDown(self):
        user_model.objects.all().delete()
        Token.objects.all().delete()

    def test_full_short_names(self):
        self.assertEqual(self.u3.get_full_name(), u'')
        self.assertEqual(self.u3.get_short_name(), self.u3.username)
        self.assertEqual(self.u2.get_full_name(), self.u2.name)
        self.assertEqual(self.u2.get_short_name(), u'User')

    def test_api_token(self):

        url = reverse('api-token')
        u4 = user_model.objects.create_user(username='User4', email='user4@foo.com', password='pass')
        u4.is_active = True
        u4.save()

        try:
            token = Token.objects.get(user=u4)
            # There should be no token for u3
            self.assertEqual(1, 0)
        except:
            pass

        resp = self.client.get(url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        ok = self.client.login(email='user4@foo.com', password='pass')
        self.assertTrue(ok)
        resp = self.client.get(url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        deserialized = json.loads(resp.content.decode())
        self.assertEqual(len(deserialized), 1)
        token = Token.objects.get(user=u4)
        self.assertEqual(deserialized['token'], token.key)
        resp = self.client.get(url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_serializer(self):
        account = Account.objects.latest('created_at')
        serialized_account = AccountSerializer(account)
        email = serialized_account.data.get('email')
        username = serialized_account.data.get('username')
        self.assertEqual(username, 'user3')
        self.assertEqual(email, 'user3@foo.com')

from rest_framework.test import APITestCase
class AccountAPITests(APITestCase):

    def setUp(self):
        self.u1 = user_model.objects.create_superuser(username='user1', email='user1@foo.com', password='pass')
        self.u1.is_active = True;
        self.u1.name = 'User One'
        self.u1.save()
        self.u2 = user_model.objects.create_user(username='user2', email='user2@foo.com', password='pass')
        self.u3 = user_model.objects.create_user(username='user3', email='user3@foo.com', password='pass')
        self.token1 = Token.objects.create(user=self.u1)
        self.token2 = Token.objects.create(user=self.u2)

    def tearDown(self):
        user_model.objects.all().delete()
        Token.objects.all().delete()


    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account-list')
        data = {'username':'user5',
                'email':'user5@foo.com',
                'password':'pass',
                'confirm_password':'pass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)

        response = self.client.get(url, data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        deserialized = json.loads((response.content).decode())
        self.assertEqual(deserialized['count'], 4)

    def test_GET_Account(self):

        url = reverse('account-detail', kwargs={'username':'user1'})
        resp = self.client.get(url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.data['id'], 1)
        self.assertEqual(resp.data['username'], u'user1')
        self.assertEqual(resp.data['email'], u'user1@foo.com')
        self.assertFalse('token' in resp.data)

    def test_PATCH_Account(self):

        url = reverse('account-detail', kwargs={'username':'user1'})

        ok = self.client.login(email='user1@foo.com', password='pass')
        self.assertTrue(ok)

        resp = self.client.get(url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['id'], 1)
        self.assertEqual(resp.data['username'], u'user1')
        self.assertEqual(resp.data['email'], u'user1@foo.com')
        self.assertEqual(resp.data['name'], u'User One')
        self.assertEqual(resp.data['tagline'], u'')

        new_tagline = 'Awesome'
        data = {'tagline':new_tagline}

        resp = self.client.patch(url, data=data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.get(url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['tagline'], new_tagline)

    def test_GET_Accounts(self):

        url = reverse('account-list')
        resp = self.client.get(url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        deserialized = json.loads(resp.content.decode())
        self.assertEqual(deserialized['count'], 3)

        self.assertEqual([obj['id'] for obj in deserialized['results']], [1,2,3])
        self.assertEqual([obj['username'] for obj in deserialized['results']], [u'user1', u'user2', u'user3'])
        self.assertEqual([obj['email'] for obj in deserialized['results']], [u'user1@foo.com',
                                                                             u'user2@foo.com',
                                                                             u'user3@foo.com'])
        self.assertFalse('token' in deserialized['results'][0])

    def test_basic_POST_Account(self):


        url = reverse('account-list')
        resp = self.client.post(url, {'username':'user4',
                                                    'email':'user4@foo.com',
                                                    'password':'pass',
                                                    'confirm_password':'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.get(url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        deserialized = json.loads(resp.content.decode())
        self.assertEqual(deserialized['count'], 4)

        # No duplicates
        data = {'username':'user4',
                'email':'user4@foo.com',
                'password':'pass',
                'confirm_password':'pass'}

        resp = self.client.post(url, data=data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        data['username'] = 'user5'
        resp = self.client.post(url, data=data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        data['username'] = 'user4'
        data['email'] = 'user5@foo.com'
        resp = self.client.post(url, data=data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        data['username'] = 'user5'
        resp = self.client.post(url, data=data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data['username'] = 'user6'
        data['email'] = 'user6@foo.com'
        data['confirm_password'] = 'pass1'
        resp = self.client.post(url, data=data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        data['tagline'] = 'Awesome'
        data['name'] = 'User One'
        data['confirm_password'] = 'pass'
        resp = self.client.post(url, data=data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_login_api(self):

        url = reverse('api-login')
        client = self.client

        resp = client.post(url, {'email':'user1@foo.com', 'password':'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        self.assertEqual(resp.data['token'], self.token1.key)

        client.logout()

        resp = client.post(url, {'email':'user1@foo.com'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = client.post(url, {'email':'user101@foo.com', 'password':'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test that we cannot login if not Active
        u5 = user_model.objects.create_user(username='user5', email='user5@foo.com', password='pass')
        u5.is_active=False
        u5.save()
        ok = client.login(email='user5@foo.com', password='pass')
        self.assertFalse(ok)
        resp = client.post(url, {'email':'user5@foo.com', 'password':'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_info_api(self):

        url = reverse('api-user-info')

        resp = self.client.get(url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        ok = self.client.login(email='user1@foo.com', password='pass')
        self.assertTrue(ok)

        resp = self.client.get(url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.data['tagline'], '')
        self.assertEqual(resp.data['name'], 'User One')
        self.assertEqual(resp.data['username'], 'user1')
        self.assertEqual(resp.data['email'], 'user1@foo.com')

    def test_PUT_Account(self):

        url = reverse('account-detail', kwargs={'username':'user1'})

        ok = self.client.login(email='user1@foo.com', password='pass')
        self.assertTrue(ok)

        resp = self.client.get(url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['id'], 1)
        self.assertEqual(resp.data['username'], u'user1')
        self.assertEqual(resp.data['email'], u'user1@foo.com')
        self.assertEqual(resp.data['name'], u'User One')
        self.assertEqual(resp.data['tagline'], u'')

        new_tagline = 'Awesome'
        data = {'email':self.u1.email,
                'username':self.u1.username,
                'name':'User One',
                'tagline':new_tagline}

        resp = self.client.put(url, data=data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.get(url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['tagline'], data['tagline'])
        self.assertEqual(resp.data['username'], data['username'])
        self.assertEqual(resp.data['name'], data['name'])
        self.assertEqual(resp.data['email'], data['email'])

    def test_logout_api(self):

        url = reverse('api-login')
        client = self.client

        resp = client.post(url, {'email':'user1@foo.com', 'password':'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        self.assertEqual(resp.data['token'], self.token1.key)

        url = reverse('api-logout')
        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

