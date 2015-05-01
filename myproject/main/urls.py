from django.conf.urls import *
from myproject.main import views
from django.views.generic import RedirectView, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
     url(r'^$', views.HomeView.as_view(), name='home'),
     # The /about URL is used for healthchecks
     url(r'^about/?$', TemplateView.as_view(template_name="main/about.html"), name='about'),

     url(r'^jsi18n', 'myproject.main.views.i18n_javascript'),
     url(r'^admin/jsi18n', 'myproject.main.views.i18n_javascript'),

)
