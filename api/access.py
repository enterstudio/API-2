from rest_framework import permissions

# Permission classes


class HausAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.users.filter(user=request.user).exists()


class DeviceAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.users.filter(user=request.user).exists()


class SensorAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.users.filter(user=request.user).exists()


class UnlimitedAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return True
