from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from clients.models import ClientApplication
from clients.serializers import CASerializer
from api.access import LCAPIPermission


class ClientApplicationList(generics.ListCreateAPIView):
    queryset = ClientApplication.objects.all()
    serializer_class = CASerializer
    permission_classes = (IsAuthenticated,
                          LCAPIPermission,)
