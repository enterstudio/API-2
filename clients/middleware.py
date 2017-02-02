from django.http import HttpResponseBadRequest, HttpResponse

from .models import ClientApplication


class ClientVerificationMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        if "HTTP_X_CLIENT_VERIFICATION" in request.META:
            if "HTTP_X_CLIENT" in request.META:
                client_id = request.META["HTTP_X_CLIENT"]
                client = ClientApplication.objects.get(pk=client_id)
                shared_secret = "\0".join((
                    request.path,
                    request.body.decode(),
                ))
                if client.verify(shared_secret,
                                 request.META["HTTP_X_CLIENT_VERIFICATION"]):
                    request.client_app = client
                else:
                    return HttpResponse("Client unverifiable.", status=401)
            else:
                return HttpResponseBadRequest("No client_id specified.")
        else:
            if "HTTP_X_CLIENT" in request.META:
                return HttpResponseBadRequest(
                    "No client verification header received"
                )
        return self.get_response(request)
