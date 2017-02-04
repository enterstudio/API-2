from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets, routers
from rest_framework import generics
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.permissions import IsAdminUser

from .models import Haus, Device, Sensor, UAC
from .serializers import *
from .access import LCAPIPermission
from .access import DevicePermission, SensorPermission, HausPermission

from clients.access import IsLazyAuthenticated
from django.db.models import Q


class HausList(generics.ListCreateAPIView):
    queryset = Haus.objects.all()
    serializer_class = HausSerializer
    permission_classes = (IsLazyAuthenticated,)

    def get_queryset(self):
        queryset = super(HausList, self).get_queryset()
        u = self.request.user
        return queryset.filter(Q(users__in=[u]) | Q(owner=u))


class HausDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Haus.objects.all()
    serializer_class = HausSerializer
    permission_classes = (IsLazyAuthenticated,
                          HausPermission,)


class DeviceList(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsLazyAuthenticated,
                          LCAPIPermission,)


class DeviceDetailByUUID(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsLazyAuthenticated,
                          DevicePermission,)
    lookup_field = 'uuid'


class DeviceListByHaus(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsLazyAuthenticated,
                          HausPermission,)
    lookup_field = 'haus'

    def get_queryset(self):
        queryset = super(DeviceListByHaus, self).get_queryset()
        return queryset.filter(haus=self.kwargs.get('haus'))


class SensorList(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (IsLazyAuthenticated,
                          LCAPIPermission,)


class SensorListByDevice(generics.ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (IsLazyAuthenticated,
                          DevicePermission,)
    lookup_field = 'device'

    def get_queryset(self):
        queryset = super(SensorListByDevice, self).get_queryset()
        return queryset.filter(device=self.kwargs.get('device'))


class SensorById(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (IsLazyAuthenticated,
                          SensorPermission,)


class UACList(generics.ListCreateAPIView):
    queryset = UAC.objects.all()
    serializer_class = UACSerializer
    permission_classes = (IsLazyAuthenticated,
                          LCAPIPermission,)


class UACDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UAC.objects.all()
    serializer_class = UACSerializer
    permission_classes = (IsLazyAuthenticated,
                          IsAdminUser,)
