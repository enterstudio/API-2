from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from api.models import Haus, Device, Sensor, UAC
from rest_framework import serializers, viewsets, routers
from django.conf.urls import url, include
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import permissions


# Some JSONResponse stuff

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


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


class HausSerializer(serializers.ModelSerializer):
    class Meta:
        model = Haus
        fields = ('id', 'name', 'owner', 'users')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('uuid', 'name', 'last_ping', 'haus')


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('id', 'device', 'name', '_category', 'last_datum')


class UACSerializer(serializers.ModelSerializer):
    class Meta:
        model = UAC
        fields = ('user', 'haus', '_level')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'is_staff')


# View classes

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


router = routers.DefaultRouter()
router.register(r'allusers', UserViewSet)


urlpatterns = [
    url(r'^haus/$', HausList.as_view()),
    url(r'^haus/(?P<pk>[0-9]+)/$', HausDetail.as_view()),
    url(r'^device/$', DeviceList.as_view()),
    url(r'^device/(?P<pk>[a-z0-9\-]+)/$', DeviceDetailByUUID.as_view()),
    url(r'^device/list/haus/(?P<haus>[0-9\-]+)/$',
        DeviceDetailByHaus.as_view()),
    url(r'^sensor/$', SensorList.as_view()),
    url(r'^sensor/list/device/(?P<device>[a-z0-9\-]+)/$',
        SensorDetailByDevice.as_view()),
    url(r'^sensor/(?P<pk>[0-9\-]+)/$', SensorById.as_view()),
    url(r'^uac/$', UACList.as_view()),
    url(r'^uac/(?P<pk>[0-9]+)/$', UACDetail.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [url(r'^', include(router.urls))]
