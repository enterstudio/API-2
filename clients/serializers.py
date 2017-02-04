from rest_framework import serializers
from clients.models import ClientApplication, ClientLoginACSRFT
from clients.models import ClientUserPermission


class CASerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientApplication
        fields = ('id', 'name', 'client_secret', 'owner')


class ClientUserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUserPermission
        fields = ('permission_type',)


class ClientLoginACSRFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientLoginACSRFT
        fields = ('auth_token',)
