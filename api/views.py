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
        fields = ('device', 'name', '_category', 'last_datum')


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
    permission_classes = (permissions.IsAdminUser,)


class HausList(generics.ListCreateAPIView):
    queryset = Haus.objects.all()
    serializer_class = HausSerializer
    permission_classes = (permissions.IsAdminUser,)


class HausDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Haus.objects.all()
    serializer_class = HausSerializer
    permission_classes = (HausAccess,)


class DeviceList(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (permissions.IsAdminUser,)


class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (DeviceAccess,)


class SensorList(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (permissions.IsAdminUser,)


class SensorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (SensorAccess,)


class UACList(generics.ListCreateAPIView):
    queryset = UAC.objects.all()
    serializer_class = UACSerializer
    permission_classes = (permissions.IsAdminUser,)


class UACDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UAC.objects.all()
    serializer_class = UACSerializer
    permission_classes = (permissions.IsAdminUser,)


router = routers.DefaultRouter()
router.register(r'allusers', UserViewSet)


urlpatterns = [
    url(r'^haus/$', HausList.as_view()),
    url(r'^haus/(?P<pk>[0-9]+)/$', HausDetail.as_view()),
    url(r'^device/$', DeviceList.as_view()),
    url(r'^device/(?P<pk>[a-z0-9\-]+)/$', DeviceDetail.as_view()),
    url(r'^sensor/$', SensorList.as_view()),
    url(r'^sensor/(?P<pk>[0-9]+)/$', SensorDetail.as_view()),
    url(r'^uac/$', UACList.as_view()),
    url(r'^uac/(?P<pk>[0-9]+)/$', UACDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [url(r'^', include(router.urls))]
