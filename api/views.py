from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets, routers
from rest_framework import generics
from rest_framework.urlpatterns import format_suffix_patterns

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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UnlimitedAccess,)


class HausList(generics.ListCreateAPIView):
    queryset = Haus.objects.all()
    serializer_class = HausSerializer
    permission_classes = (UnlimitedAccess,)


class HausDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Haus.objects.all()
    serializer_class = HausSerializer
    permission_classes = (UnlimitedAccess,)


class DeviceList(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (UnlimitedAccess,)


class DeviceDetailByUUID(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (UnlimitedAccess,)
    lookup_field = 'uuid'


class DeviceDetailByHaus(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (UnlimitedAccess,)
    lookup_field = 'haus'

    def get_queryset(self):
        queryset = super(DeviceDetailByHaus, self).get_queryset()
        return queryset.filter(haus=self.kwargs.get('haus'))


class SensorList(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (UnlimitedAccess,)


class SensorDetailByDevice(generics.ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (UnlimitedAccess,)
    lookup_field = 'device'

    def get_queryset(self):
        queryset = super(SensorDetailByDevice, self).get_queryset()
        return queryset.filter(device=self.kwargs.get('device'))


class SensorById(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (UnlimitedAccess,)


class UACList(generics.ListCreateAPIView):
    queryset = UAC.objects.all()
    serializer_class = UACSerializer
    permission_classes = (UnlimitedAccess,)


class UACDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UAC.objects.all()
    serializer_class = UACSerializer
    permission_classes = (UnlimitedAccess,)
