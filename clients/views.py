from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from clients.models import ClientApplication, ClientLoginACSRFT
from clients.serializers import CASerializer, ClientLoginACSRFTSerializer
from clients.access import IsClient
from api.access import LCAPIPermission


class ClientApplicationList(generics.ListCreateAPIView):
    queryset = ClientApplication.objects.all()
    serializer_class = CASerializer
    permission_classes = (IsAuthenticated,
                          LCAPIPermission,)


class ClientGenToken(generics.CreateAPIView):
    queryset = ClientLoginACSRFT.objects.all()
    serializer_class = ClientLoginACSRFTSerializer
    permission_classes = (IsClient,)

    def perform_create(self, serializer):
        instance = serializer.save(client=self.request.client)
        return instance
