import json
try:
    from urlparse import urlparse as urlparse
except ImportError:
    from urllib.parse import urlparse as urlparse

from django.contrib.auth.models import User

from django.contrib.auth import authenticate

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.views import View
from django.http import HttpResponse

from clients.models import ClientApplication, ClientLoginACSRFT
from clients.models import ClientUserAuthentication
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


class ClientLogin(View):

    def post(self, request):
        jsn = json.loads(request.body.decode())
        if all(x in jsn for x in ["username", "password", "client"]):
            u = authenticate(username=jsn["username"],
                             password=jsn["password"])
            # hASHTAG Security
            client = ClientApplication.objects.get(id=jsn["client"])
            parsed_uri = urlparse(request.META["HTTP_REFERER"])
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            if client.domain != domain:
                return HttpResponse('Unauthorized', status=401)
            if ClientLoginACSRFT.objects.filter(
                auth_token=jsn["token"]
            ).exists() and u is not None:
                cua = ClientUserAuthentication(
                    client=ClientApplication.objects.get(id=jsn["client"]),
                    user=User.objects.get(username=jsn["username"])
                )
                return HttpResponse(
                    json.dumps({"auth_token": cua.auth_token})
                )
        return HttpResponse('Unauthorized', status=401)
