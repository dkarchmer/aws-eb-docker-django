__author__ = 'david'

import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework import views
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route

from django.conf import settings

from authentication.models import Account
from authentication.permissions import IsAccountOwner
from authentication.serializers import *

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class APITokenViewSet(APIView):
    """
    View to get User's token
    """

    def get(self, request, format=None):
        """
        Update thumbnail and tiny file field
        """
        if request.user.is_anonymous():
            # User most login before they can get a token
            # This not only ensures the user has registered, and has an account
            # but that the account is active
            return JSONResponse('User not recognized.', status=status.HTTP_403_FORBIDDEN)

        data_dic = {}

        try:
            token = Token.objects.get(user=request.user)
            mystatus = status.HTTP_200_OK
        except:
            token = Token.objects.create(user=request.user)
            mystatus = status.HTTP_201_CREATED

        data_dic['token'] = token.key
        return JSONResponse(data_dic, status=mystatus)

class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    @csrf_exempt
    def create(self, request):
        '''
        When you create an object using the serializer's .save() method, the
        object's attributes are set literally. This means that a user registering with
        the password 'password' will have their password stored as 'password'. This is bad
        for a couple of reasons: 1) Storing passwords in plain text is a massive security
        issue. 2) Django hashes and salts passwords before comparing them, so the user
        wouldn't be able to log in using 'password' as their password.

        We solve this problem by overriding the .create() method for this viewset and
        using Account.objects.create_user() to create the Account object.
        '''

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['confirm_password']

            if password and confirm_password and password == confirm_password:

                # Note that for now, Accounts default to is_active=False
                # which means that we need to manually active them
                # This is to keep the site secure until we go live
                account = Account.objects.create_user(**serializer.validated_data)

                account.set_password(serializer.validated_data['password'])
                account.save()


                return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({'status': 'Bad request',
                         'message': 'Account could not be created with received data.'
                        }, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def set_password(self, request, username=None):
        account = self.get_object()
        serializer = PasswordCustomSerializer(data=request.data)
        if serializer.is_valid():
            account.set_password(serializer.data['password'])
            account.save()

            return Response({'status': 'password set'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APILoginViewSet(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    #permission_classes = ()

    @csrf_exempt
    def post(self, request, format=None):
        """
        Update thumbnail and tiny file field
        """
        data = JSONParser().parse(request)
        serializer = LoginCustomSerializer(data=data)

        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            if not request.user.is_anonymous():
                return JSONResponse('Already Logged-in', status=status.HTTP_403_FORBIDDEN)

            account = authenticate(email=email, password=password)

            if account is not None:
                if account.is_active:
                    login(request, account)

                    serialized = AccountSerializer(account)
                    data = serialized.data

                    # Add the token to the return serialization
                    try:
                        token = Token.objects.get(user=account)
                    except:
                        token = Token.objects.create(user=account)

                    data['token'] = token.key


                    return Response(data)
                else:
                    return JSONResponse('This account is not Active.', status=status.HTTP_401_UNAUTHORIZED)
            else:
                return JSONResponse('Username/password combination invalid.', status=status.HTTP_401_UNAUTHORIZED)

        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        """
        Update thumbnail and tiny file field
        """

        data_dic = {"Error":"GET not supported for this command"}

        logout(request)
        mystatus = status.HTTP_400_BAD_REQUEST

        return JSONResponse(data_dic, status=mystatus)


class APILogoutViewSet(APIView):
    """
    View to get User's token
    """

    def get(self, request, format=None):
        """
        Update thumbnail and tiny file field
        """
        if request.user.is_anonymous():
            return JSONResponse('User not recognized.', status=status.HTTP_403_FORBIDDEN)


        data_dic = {}

        logout(request)
        mystatus = status.HTTP_200_OK

        return JSONResponse(data_dic, status=mystatus)


class APIUserInfoViewSet(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    #permission_classes = ()

    def get(self, request, format=None):
        """
        Update thumbnail and tiny file field
        """
        if request.user.is_anonymous():
            # User most login before they can get a token
            # This not only ensures the user has registered, and has an account
            # but that the account is active
            return JSONResponse('User not recognized.', status=status.HTTP_403_FORBIDDEN)

        account = request.user

        serialized = AccountSerializer(account)
        data = serialized.data

        # Add the token to the return serialization
        try:
            token = Token.objects.get(user=account)
        except:
            token = Token.objects.create(user=account)

        data['token'] = token.key

        return Response(data)

