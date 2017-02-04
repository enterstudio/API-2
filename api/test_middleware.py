from django.urls import reverse

from lazy_extensions.lazy_api_test import LazyAPITestBase, RequestAssertion

from .models import Device, Sensor


class VerificationMiddlewareTest(LazyAPITestBase):
    def test_security(self):
        device = Device.objects.create_device("a")
        device.save()
        fake_device = Device.objects.create_device("b")
        fake_device.save()

        sensor = Sensor.objects.create_sensor(device, "c", 0)
        sensor.save()

        url = reverse("sensor-detail", kwargs={"pk": sensor.pk})

        ra = RequestAssertion(self.client, url=url, method="GET")

        shared_secret = "\0".join((
            url,
            "",
        ))
        valid_signature = device.sign(shared_secret)
        invalid_signature_message = device.sign("Other message")
        invalid_signature_device = fake_device.sign(shared_secret)
        invalid_signature_device_message = fake_device.sign("Other message")

        # No device, no signature
        ra.update(status=403, kwargs={})
        # No device, signature
        ra.update(status=400, kwargs={
            'HTTP_X_DEVICE_VERIFICATION': valid_signature,
        }).execute()
        # device, no signature
        ra.update(status=403, kwargs={
            'HTTP_X_DEVICE': str(device.pk),
        }).execute()
        # device, signature
        ra.update(status=200, kwargs={
            'HTTP_X_DEVICE': str(device.pk),
            'HTTP_X_DEVICE_VERIFICATION': valid_signature,
        }).execute()

        # Wrong Client, correct signature
        ra.update(status=401, kwargs={
            'HTTP_X_DEVICE': str(fake_device.pk),
            'HTTP_X_DEVICE_VERIFICATION': valid_signature,
        }).execute()

        for signature in [
            invalid_signature_device,
            invalid_signature_message,
            invalid_signature_device_message,
        ]:
            ra.update(status=401, kwargs={
                'HTTP_X_DEVICE': str(device.pk),
                'HTTP_X_DEVICE_VERIFICATION': signature,
            })
