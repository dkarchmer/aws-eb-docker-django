__author__ = 'david'

from django.conf.urls import *
from authentication.api_views import APILoginViewSet, APILogoutViewSet, APITokenViewSet, APIUserInfoViewSet

urlpatterns = patterns('',
    url(r'^login$', APILoginViewSet.as_view(), name='api-login'),
    url(r'^logout$', APILogoutViewSet.as_view(), name='api-logout'),
    url(r'^token$', APITokenViewSet.as_view(), name='api-token'),
    url(r'^user-info$', APIUserInfoViewSet.as_view(), name='api-user-info'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token', name='api-token-auth'),

)
