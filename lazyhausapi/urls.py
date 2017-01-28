from django.conf.urls import url, include
from django.contrib.auth.models import User
from api.models import Haus, Device, Sensor, UAC
from rest_framework import serializers, viewsets, routers


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class HausSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Haus
        fields = ('name', 'owner', 'users')


# ViewSets define the view behavior.
class HausViewSet(viewsets.ModelViewSet):
    queryset = Haus.objects.all()
    serializer_class = HausSerializer


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('uuid', 'name', 'last_ping', 'haus')


# ViewSets define the view behavior.
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class SensorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sensor
        fields = ('device', 'name', 'category', 'last_datum')


# ViewSets define the view behavior.
class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer




# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'haus',  HausViewSet)
router.register(r'device', DeviceViewSet)
router.register(r'sensor', SensorViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
]
