from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets, routers
from rest_framework import generics
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Haus, Device, Sensor, UAC
from .serializers import *
from .access import LCAPIPermission
from .access import DevicePermission, SensorPermission, HausPermission

# Some JSONResponse stuff


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class HausList(generics.ListCreateAPIView):
    queryset = Haus.objects.all()
    serializer_class = HausSerializer
    permission_classes = (IsAuthenticated,
                          LCAPIPermission,)


class HausDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Haus.objects.all()
    serializer_class = HausSerializer
    permission_classes = (IsAuthenticated,
                          HausPermission,)


class DeviceList(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,
                          LCAPIPermission,)


class DeviceDetailByUUID(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,
                          DevicePermission,)
    lookup_field = 'uuid'


class DeviceListByHaus(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,
                          HausPermission,)
    lookup_field = 'haus'

    def get_queryset(self):
        queryset = super(DeviceListByHaus, self).get_queryset()
        return queryset.filter(haus=self.kwargs.get('haus'))


class SensorList(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (IsAuthenticated,
                          LCAPIPermission,)


class SensorListByDevice(generics.ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (IsAuthenticated,
                          DevicePermission,)
    lookup_field = 'device'

    def get_queryset(self):
        queryset = super(SensorListByDevice, self).get_queryset()
        return queryset.filter(device=self.kwargs.get('device'))


class SensorById(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (IsAuthenticated,
                          SensorPermission,)


class UACList(generics.ListCreateAPIView):
    queryset = UAC.objects.all()
    serializer_class = UACSerializer
    permission_classes = (IsAuthenticated,
                          LCAPIPermission,)


class UACDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UAC.objects.all()
    serializer_class = UACSerializer
    permission_classes = (IsAuthenticated,
                          IsAdminUser,)
