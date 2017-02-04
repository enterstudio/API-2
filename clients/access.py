from rest_framework import permissions


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, 'client')


class IsLazyAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, 'user')
