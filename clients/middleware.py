import json

from django.http import HttpResponseBadRequest, HttpResponse

from .models import ClientApplication, ClientUserAuthentication

from lazy_extensions.lazy_errors import errors


class ClientVerificationMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        if "HTTP_X_CLIENT_VERIFICATION" in request.META:
            if "HTTP_X_CLIENT" in request.META:
                client_id = request.META["HTTP_X_CLIENT"]
                client = ClientApplication.objects.get(pk=client_id)
                if client.verify_request(
                        request, request.META["HTTP_X_CLIENT_VERIFICATION"]):
                    request.client = client
                else:
                    return HttpResponse(json.dumps({
                        "error": errors[0],
                    }), status=401)
            else:
                return HttpResponseBadRequest(json.dumps({
                    "error": errors[1],
                }))
        return self.get_response(request)


class ClientUserAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "HTTP_X_AUTH_TOKEN" in request.META:
            if "HTTP_X_CLIENT" not in request.META:
                return HttpResponseBadRequest(json.dumps({
                    "error": errors[1],
                }))
            client_pk = request.META["HTTP_X_CLIENT"]
            try:
                cua = ClientUserAuthentication.objects.get(
                    client=client_pk,
                    auth_token=request.META["HTTP_X_AUTH_TOKEN"]
                )
            except ClientUserAuthentication.DoesNotExist:
                return HttpResponse(json.dumps({
                    "error": errors[2],
                }), status=401)
            request.user = cua.user
            request.user.current_authentication = cua
        return self.get_response(request)
