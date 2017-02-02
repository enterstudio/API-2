from lazy_extensions.lazy_api_test import LazyAPITestBase, RequestAssertion

from .models import ClientApplication, ClientUserAuthentication


class VerificationMiddlewareTest(LazyAPITestBase):
    def test_security(self):
        admin, _ = self.create_admin_and_user()

        client = ClientApplication(owner=admin, name="a")
        client.save()
        fake_client = ClientApplication(owner=admin, name="a")
        fake_client.save()

        ra = RequestAssertion(self.client, url="/", method="GET")

        shared_secret = "\0".join((
            "/",
            "",
        ))
        valid_signature = client.sign(shared_secret)
        invalid_signature_message = client.sign("Other message")
        invalid_signature_client = fake_client.sign(shared_secret)
        invalid_signature_client_message = fake_client.sign("Other message")
        # No client, no signature
        ra.update(status=403, kwargs={})
        # No Client, signature
        ra.update(status=400, kwargs={
            'HTTP_X_CLIENT_VERIFICATION': valid_signature,
        }).execute()
        # Client, no signature
        ra.update(status=403, kwargs={
            'HTTP_X_CLIENT': str(client.pk),
        }).execute()
        # Client, signature
        ra.update(status=403, kwargs={
            'HTTP_X_CLIENT': str(client.pk),
            'HTTP_X_CLIENT_VERIFICATION': valid_signature,
        }).execute()

        # Wrong Client, correct signature
        ra.update(status=401, kwargs={
            'HTTP_X_CLIENT': str(fake_client.pk),
            'HTTP_X_CLIENT_VERIFICATION': valid_signature,
        }).execute()

        for signature in [
            invalid_signature_client,
            invalid_signature_message,
            invalid_signature_client_message,
        ]:
            ra.update(status=401, kwargs={
                'HTTP_X_CLIENT': str(client.pk),
                'HTTP_X_CLIENT_VERIFICATION': signature,
            })

        token = ClientUserAuthentication(client=client, user=admin)
        token.save()

        ra.update(status=200, kwargs={
            'HTTP_X_CLIENT': str(client.pk),
            'HTTP_X_AUTH_TOKEN': token.auth_token,
        }).execute()

        ra.update(status=400, kwargs={
            'HTTP_X_AUTH_TOKEN': '',
        }).execute()

        ra.update(status=401, kwargs={
            'HTTP_X_CLIENT': str(client.pk),
            'HTTP_X_AUTH_TOKEN': "RANDOMTOKEN",
        }).execute()

        ra.update(status=401, kwargs={
            'HTTP_X_CLIENT': str(fake_client.pk),
            'HTTP_X_AUTH_TOKEN': token.auth_token,
        }).execute()

        ra.update(status=401, kwargs={
            'HTTP_X_CLIENT': str(fake_client.pk),
            'HTTP_X_AUTH_TOKEN': "RANDOMTOKEN",
        }).execute()
