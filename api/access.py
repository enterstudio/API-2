from rest_framework import permissions

# Permission classes

# ListCreateAPIView Permission
# Essentially the permissions on listing "all of the things"


class LCAPIPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            # Allow post
            return True
        if request.method == 'GET':
            # Only staff can get an entire list
            return request.user.is_staff
        return False

# The rest of these permissions should be updated appropriately
# when further specification of permissions on sensors are described
# i.e what access does a landlord have


class HausPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.users.filter(id=request.user.id).exists()


class DevicePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.haus.users.filter(id=request.user.id).exists()


class SensorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.device.haus.users.filter(id=request.user.id).exists()


class UnlimitedPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return True
