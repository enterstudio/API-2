from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets, routers
from rest_framework import generics
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.permissions import IsAdminUser

from .models import Haus, Device, Sensor, UAC
from .access import UnlimitedAccess
from .serializers import *

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
    permission_classes = (IsAdminUser,)


class HausDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Haus.objects.all()
    serializer_class = HausSerializer
    permission_classes = (UnlimitedAccess,)


class DeviceList(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsAdminUser,)


class DeviceDetailByUUID(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (UnlimitedAccess,)
    lookup_field = 'uuid'


class DeviceListByHaus(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (UnlimitedAccess,)
    lookup_field = 'haus'

    def get_queryset(self):
        queryset = super(DeviceListByHaus, self).get_queryset()
        return queryset.filter(haus=self.kwargs.get('haus'))


class SensorList(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (IsAdminUser,)


class SensorListByDevice(generics.ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (UnlimitedAccess,)
    lookup_field = 'device'

    def get_queryset(self):
        queryset = super(SensorListByDevice, self).get_queryset()
        return queryset.filter(device=self.kwargs.get('device'))


class SensorById(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (UnlimitedAccess,)


class UACList(generics.ListCreateAPIView):
    queryset = UAC.objects.all()
    serializer_class = UACSerializer
    permission_classes = (IsAdminUser,)


class UACDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UAC.objects.all()
    serializer_class = UACSerializer
    permission_classes = (UnlimitedAccess,)
