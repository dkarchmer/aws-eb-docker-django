
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import DetailView, TemplateView
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib import admin
from django.conf import settings
from django.views.generic import View
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie

from myproject.main.models import *
from myproject.main.forms import *

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class HomeView(View):
    def get(self, request):
        production = settings.PRODUCTION
        user = request.user

        if user.is_authenticated():
            template = 'main/index.html'
        else:
            template = 'main/landing.html'

        return render_to_response(template, locals(), context_instance = RequestContext(request))

def i18n_javascript(request):
    return admin.site.i18n_javascript(request)

