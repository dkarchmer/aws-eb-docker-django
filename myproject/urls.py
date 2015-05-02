from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin

from myproject.main.api_views import APIMessageViewSet
from authentication.api_views import AccountViewSet


# Rest APIs
# =========
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf
v1_api_router = routers.DefaultRouter(trailing_slash=False)
v1_api_router.register(r'message', APIMessageViewSet)
v1_api_router.register(r'account', AccountViewSet)

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    url(r'^', include('myproject.main.urls')),
    url(r'^account/', include('authentication.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/v1/', include(v1_api_router.urls)),
    url(r'^api/v1/auth/', include('authentication.api_urls')),

    url('^robots.txt$', TemplateView.as_view(template_name="robots.txt")),

)
