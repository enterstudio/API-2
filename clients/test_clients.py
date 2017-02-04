from django.urls import reverse

from rest_framework import status

from lazy_extensions.lazy_api_test import LazyAPITestBase, RequestAssertion

from clients.models import ClientApplication, ClientLoginACSRFT


class PermissionTests(LazyAPITestBase):
    def test_lcdapi_admin_only(self):
        self.create_admin_and_user()

        self.login_admin()
        urls = [reverse(x + "-lcdapi")
                for x in ["ca"]]

        ra = RequestAssertion(self.client, method="GET", status=200)
        for url in urls:
            ra.update(url=url).execute()
        self.login_user()
        ra.update(status=status.HTTP_403_FORBIDDEN)
        for url in urls:
            ra.update(url=url).execute()

    def test_token_gen(self):
        admin, _ = self.create_admin_and_user()
        client = ClientApplication(owner=admin, name="a")
        client.save()

        ra = RequestAssertion(
            self.client, url=reverse("clacsrft"), method="POST", status=201
        )
        auth_token = ra.update(kwargs={
            'HTTP_X_CLIENT': str(client.pk),
            'HTTP_X_CLIENT_VERIFICATION': client.sign("\0".join((
                ra.url,
                '{}',
            ))),
        }).execute().response.data["auth_token"]

    def test_login(self):
        admin, _ = self.create_admin_and_user()
        client = ClientApplication(owner=admin, name="a")
        client.save()

        ra = RequestAssertion(
            self.client, url=reverse("clacsrft"), method="POST", status=201
        )
        auth_token = ra.update(kwargs={
            'HTTP_X_CLIENT': str(client.pk),
            'HTTP_X_CLIENT_VERIFICATION': client.sign("\0".join((
                ra.url,
                '{}',
            ))),
        }).execute().response.data["auth_token"]

        RequestAssertion(self.client).update(
            kwargs={'HTTP_REFERER': "https://example.com"},
            method="POST",
            url=reverse('ca-login'),
            data={"username": "Bojangle", "password": "pass",
                  "token": auth_token, "client": str(client.pk)
                  }
        ).execute().update(
            status=401,
            data={"username": "Bojangles", "password": "Nob",
                  "token": auth_token, "client": str(client.pk)
                  }
        ).execute().update(
            status=200,
            data={"username": "straycat", "password": "pass",
                  "token": auth_token, "client": str(client.pk)
                  }
        ).execute().update(
            status=401,
            data={"username": "straycat", "password": "pass",
                  "token": "bad", "client": str(client.pk)
                  }
        ).execute()
