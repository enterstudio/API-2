from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Haus, Device, Sensor, UAC


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
        fields = ('id', 'device', 'name', 'category', 'last_datum')


class UACSerializer(serializers.ModelSerializer):
    class Meta:
        model = UAC
        fields = ('user', 'haus', 'level')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'is_staff')


# View classes
