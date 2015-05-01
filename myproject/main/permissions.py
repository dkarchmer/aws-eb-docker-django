__author__ = 'david'

from rest_framework import permissions


class ContactMessagePermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access (read/write)
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        else:
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Everybody can submit
        return request.user.is_staff
