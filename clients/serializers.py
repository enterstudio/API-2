from rest_framework import serializers
from clients.models import ClientApplication


class CASerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientApplication
        fields = ('id', 'name', 'client_secret', 'owner')
