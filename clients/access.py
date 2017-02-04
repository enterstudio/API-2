from rest_framework import permissions

from django.contrib.auth.models import AnonymousUser


class IsClient(permissions.BasePermission):
    @classmethod
    def has_permission(self, request, view):
        return hasattr(request, 'client')


class IsLazyAuthenticated(permissions.BasePermission):
    @classmethod
    def has_permission(self, request, view):
        if request.device is not None:
            return True
        return not isinstance(request.user, AnonymousUser)
