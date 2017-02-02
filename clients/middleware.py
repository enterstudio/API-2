from django.http import HttpResponseBadRequest, HttpResponse

from .models import ClientApplication, ClientUserAuthentication


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
                    print(request.path, request.body)
                    return HttpResponse("Client unverifiable.", status=401)
            else:
                return HttpResponseBadRequest("No client_id specified.")
        return self.get_response(request)


class ClientUserAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "HTTP_X_AUTH_TOKEN" in request.META:
            if "HTTP_X_CLIENT" not in request.META:
                return HttpResponseBadRequest("No client id")
            client_pk = request.META["HTTP_X_CLIENT"]
            try:
                cua = ClientUserAuthentication.objects.get(
                    client=client_pk,
                    auth_token=request.META["HTTP_X_AUTH_TOKEN"]
                )
            except ClientUserAuthentication.DoesNotExist:
                return HttpResponse("Invalid auth token.", status=401)
            request.user = cua.user
            request.user.current_authentication = cua
        return self.get_response(request)
