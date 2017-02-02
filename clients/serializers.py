from rest_framework import serializers
from clients.models import ClientApplication, ClientLoginACSRFT


class CASerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientApplication
        fields = ('id', 'name', 'client_secret', 'owner')


class ClientLoginACSRFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientLoginACSRFT
        fields = ('auth_token',)
