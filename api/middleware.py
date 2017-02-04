from django.http import HttpResponseBadRequest, HttpResponse

from .models import Device


class DeviceVerificationMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        if "HTTP_X_DEVICE_VERIFICATION" in request.META:
            if "HTTP_X_DEVICE" in request.META:
                device_id = request.META["HTTP_X_DEVICE"]
                device = Device.objects.get(pk=device_id)
                if device.verify_request(
                        request, request.META["HTTP_X_DEVICE_VERIFICATION"]):
                    request.device = device
                else:
                    return HttpResponse("Device unverifiable.", status=401)
            else:
                return HttpResponseBadRequest("No device_id specified.")
        return self.get_response(request)
