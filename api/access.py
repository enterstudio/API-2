from rest_framework import permissions
from .models import Device, Sensor, Haus

# Permission classes

# ListCreateAPIView Permission
# Essentially the permissions on listing "all of the things"


class LCAPIPermission(permissions.BasePermission):
    @classmethod
    def has_permission(cls, request, view):
        if request.method == 'POST':
            # Allow post
            return True
        if request.method == 'GET':
            # Only staff can get an entire list
            return request.user.is_staff

# The rest of these permissions should be updated appropriately
# when further specification of permissions on sensors are described
# i.e what access does a landlord have


class HausPermission(permissions.BasePermission):
    @classmethod
    def has_permission(cls, request, view):
        haus = Haus.objects.get(id=view.kwargs.get(view.lookup_field))
        return haus.users.filter(id=request.user.id).exists()

    @classmethod
    def has_object_permission(cls, request, view, obj):
        return obj.users.filter(id=request.user.id).exists()


class DevicePermission(permissions.BasePermission):
    @classmethod
    def has_permission(cls, request, view):
        device = Device.objects.get(uuid=view.kwargs.get(view.lookup_field))
        return device.haus.users.filter(id=request.user.id).exists()

    @classmethod
    def has_object_permission(cls, request, view, obj):
        return obj.haus.users.filter(id=request.user.id).exists()


class SensorPermission(permissions.BasePermission):
    @classmethod
    def has_permission(cls, request, view):
        sensor = Sensor.objects.get(id=view.kwargs.get(view.lookup_field))
        if request.device is not None:
            return sensor.device == request.device and request.method in (
                "PUT",
                "POST",
                "OPTIONS",
                "GET",
            )
        return sensor.device.haus.users.filter(id=request.user.id).exists()

    @classmethod
    def has_object_permission(cls, request, view, obj):
        if request.device is not None:
            return obj.device == request.device and request.method in (
                "PUT",
                "POST",
                "OPTIONS",
                "GET",
            )
        return obj.device.haus.users.filter(id=request.user.id).exists()


# class UnlimitedPermission(permissions.BasePermission):
#     def has_object_permission(cls, request, view, obj):
#         return True
