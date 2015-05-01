__author__ = 'david'

from django import forms as forms
from django.forms import ModelForm
from authentication.models import Account

class AccountUpdateForm(ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'name', 'tagline']

    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

class AvatarUpdateForm(ModelForm):
    class Meta:
        model = Account
        fields = ['avatar_original']

    def __init__(self, *args, **kwargs):
        super(AvatarUpdateForm, self).__init__(*args, **kwargs)

class AvatarForm(forms.Form):
    avatar_url = forms.CharField(max_length=200)
    profile_id = forms.CharField(max_length=20)

