from rest_framework import permissions

# Permission classes


class HausAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.users.all()


class DeviceAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.haus.users.all()


class SensorAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.device.haus.users.all()


class UnlimitedAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return True
