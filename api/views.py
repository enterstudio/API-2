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

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class HausSerializer(serializers.ModelSerializer):
    class Meta:
        model = Haus
        fields = ('id', 'name', 'owner', 'users')


# ViewSets define the view behavior.
class HausViewSet(viewsets.ModelViewSet):
    queryset = Haus.objects.all()
    serializer_class = HausSerializer


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('uuid', 'name', 'last_ping', 'haus')


# ViewSets define the view behavior.
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('device', 'name', 'category', 'last_datum')


# ViewSets define the view behavior.
class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

@csrf_exempt

@api_view(['GET', 'POST'])
def haus_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        hauses = Haus.objects.all()
        serializer = HausSerializer(hauses, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = HausSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def haus_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        haus = Haus.objects.get(pk=pk)
    except Haus.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = HausSerializer(haus)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = HausSerializer(haus, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        haus.delete()
        return HttpResponse(status=204)


router = routers.DefaultRouter()
router.register(r'allusers', UserViewSet)


urlpatterns = [
    url(r'^haus/$', haus_list),
    url(r'^haus/(?P<pk>[0-9]+)/$', haus_detail),
    url(r'^', include(router.urls)),
]
