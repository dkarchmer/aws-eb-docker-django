import os
from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView, FormView
from django.views.generic import DetailView, TemplateView, RedirectView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from authentication.models import Account
from authentication.forms import *

class AccountRedirectView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user

        return HttpResponseRedirect(reverse('account_detail', args=(user.username,)))


class AccountDetailView(DetailView):
    model = Account
    template_name = 'authentication/detail.html'

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AccountDetailView, self).dispatch(request, *args, **kwargs)

class AccountUpdateView(UpdateView):
    model = Account
    form_class = AccountUpdateForm
    template_name = 'authentication/form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AccountUpdateView, self).dispatch(request, *args, **kwargs)

