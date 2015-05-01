from django.contrib import admin
from authentication.models import *

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'name', 'created_at', 'last_login')


"""
Register Admin Pages
"""
admin.site.register(Account, AccountAdmin)
