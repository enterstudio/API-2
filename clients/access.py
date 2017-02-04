from rest_framework import permissions

from django.contrib.auth.models import AnonymousUser


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, 'client')


class IsLazyAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return not isinstance(request.user, AnonymousUser)
