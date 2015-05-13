__author__ = 'David Karchmer'

from django.conf.urls import *
from django.views.generic import RedirectView, TemplateView
from django.core.urlresolvers import reverse_lazy

from authentication.views import *

urlpatterns = patterns('',

     url(r'^$', AccountRedirectView.as_view(), name='account_redirect'),
     url(r'^init/?$', AccountInitView.as_view(), name='account_init'),

     url(
        r'^login/$','django.contrib.auth.views.login',
        dict(
            template_name = 'registration/login.html',
        ),
        name='login',
     ),
     url(
        r'^logout/$','django.contrib.auth.views.logout',
        dict(
            next_page = '/',
        ),
        name='logout',
     ),
     url(r'^(?P<slug>\w+)/edit/?$', AccountUpdateView.as_view(), name='account_edit'),
     url(r'^(?P<slug>\w+)/?$', AccountDetailView.as_view(), name='account_detail'),

)
