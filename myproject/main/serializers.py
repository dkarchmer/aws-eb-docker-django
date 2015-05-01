__author__ = 'david'

from rest_framework import serializers

from myproject.main.models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ('id', 'name', 'email', 'phone', 'message', 'created_on')
        read_only_fields = ('created_on')

