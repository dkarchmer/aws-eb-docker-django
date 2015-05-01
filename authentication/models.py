import os
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.template.defaultfilters import slugify
# import code for encoding urls and generating md5 hashes
import hashlib
try:
    # Python 3.4
    import urllib.parse
except ImportError:
    # Python 2.7
    import urllib

from django.templatetags.static import static
from django.utils.encoding import python_2_unicode_compatible


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_admin = True
        account.is_active = True
        account.is_staff = True
        account.save()

        return account

@python_2_unicode_compatible
class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=60)

    name = models.CharField(verbose_name='Full Name', max_length=120, blank=True)
    tagline = models.CharField(max_length=260, blank=True)

    avatar_original = models.CharField(max_length=260, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):

        self.slug = slugify(self.username)

        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        if (self.name != ''):
            # Try to extract the first name
            names = self.name.split()
            first_name = names[0]
            return first_name
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(perm_list, obj=None):
        print(str(perm_list))
        return True

    def has_module_perms(self, app_label):
        return True

    # Custom Methods
    # --------------
    def get_absolute_url(self):
        return '/account/%s/' % self.username

    def get_edit_url(self):
        return '%sedit/' % self.get_absolute_url()

    def get_thumbnail_url(self):
        #key = bucket.new_key(self.avatar)
        #url = key.generate_url(expires_in=0, query_auth=False)
        file_name = None
        return self.get_gravatar_thumbnail_url()

    def get_picture_upload_url(self):
        return '%savatar/upload/' % self.get_absolute_url()

    def get_avatar_file_name(self):
        return 'avatar-%s' % self.username

    def get_gravatar_thumbnail_url(self, size=100):
        # Set your variables here
        email = self.email
        default = 'identicon'

        # construct the url
        gravatar_url = "https://secure.gravatar.com/avatar/" + hashlib.md5(email.lower().encode('utf-8')).hexdigest() + "?"
        try:
            # Python 3.4
            gravatar_url += urllib.parse.urlencode({'d':default, 's':str(size)})
        except:
            # Python 2.7
            gravatar_url += urllib.urlencode({'d':default, 's':str(size)})

        return gravatar_url