from rest_framework import permissions


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request)
        return hasattr(request, 'client')
