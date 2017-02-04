import functools

import json

from django.urls import reverse

from rest_framework import status

from lazy_extensions.lazy_api_test import LazyAPITestBase, RequestAssertion

from clients.models import ClientApplication
from clients.models import ClientUserPermission, ClientUserAuthentication


class PermissionTests(LazyAPITestBase):

    @classmethod
    def get_auth_token(self, client, ra):
        return ra.update(kwargs={
            'HTTP_X_CLIENT': str(client.pk),
            'HTTP_X_CLIENT_VERIFICATION': client.sign("\0".join((
                ra.url,
                '{}',
            ))),
        }).execute().response.data["auth_token"]

    def test_lcdapi_admin_only(self):
        admin, _ = self.create_admin_and_user()

        client = ClientApplication(owner=admin, name="a")
        client.save()
        self.login_admin(client)
        urls = [reverse(x + "-lcdapi")
                for x in ["ca"]]

        ra = RequestAssertion(self.client, method="GET", status=200)
        for url in urls:
            ra.update(url=url).execute()
        self.login_user(client)
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
        self.get_auth_token(client, ra)

    def test_login(self):
        admin, _ = self.create_admin_and_user()
        client = ClientApplication(owner=admin, name="a")
        client.save()

        auth_ra = RequestAssertion(
            self.client, url=reverse("clacsrft"), method="POST", status=201
        )
        self.get_auth_token(client, auth_ra)
        at = functools.partial(self.get_auth_token, client, auth_ra)

        RequestAssertion(self.client).update(  # Good
            kwargs={'HTTP_REFERER': "https://example.com"},
            method="POST",
            url=reverse('ca-login'),
            data={"username": "Bojangle", "password": "pass",
                  "token": at(), "client": str(client.pk)
                  }
        ).execute().update(  # Bad password
            status=401,
            data={"username": "Bojangles", "password": "Nob",
                  "token": at(), "client": str(client.pk)
                  }
        ).execute().update(  # Good
            status=200,
            data={"username": "straycat", "password": "pass",
                  "token": at(), "client": str(client.pk)
                  }
        ).execute().update(  # Bad token
            status=401,
            data={"username": "straycat", "password": "pass",
                  "token": "bad", "client": str(client.pk)
                  }
        ).execute().update(  # Bad referrer
            kwargs={'HTTP_REFERER': "https://baddomain.com"},
            status=401,
            data={"username": "straycat", "password": "pass",
                  "token": at(), "client": str(client.pk)
                  }
        ).execute()

        ClientUserAuthentication.objects.all().delete()

        ra = RequestAssertion(self.client).update(
            kwargs={'HTTP_REFERER': "https://example.com"},
            method="POST",
            url=reverse('ca-logout'),
        )
        #  Login and Logout in succession
        for _ in range(3):
            self.login_user(client)
            ra.execute()
        # Now that the uac doesn't exist, must return 401
        ra.update(status=401).execute()

    def test_get_permissions(self):
        admin, _ = self.create_admin_and_user()
        client = ClientApplication(owner=admin, name="a")
        client.save()

        auth_ra = RequestAssertion(
            self.client, url=reverse("clacsrft"), method="POST", status=201
        )
        csrf_token = self.get_auth_token(client, auth_ra)

        auth_token = json.loads(RequestAssertion(self.client).update(  # Good
            kwargs={'HTTP_REFERER': "https://example.com"},
            method="POST",
            url=reverse('ca-login'),
            data={"username": "Bojangle", "password": "pass",
                  "token": csrf_token, "client": str(client.pk)
                  }
        ).execute().response.content.decode())["auth_token"]

        print(ClientUserAuthentication.objects.first())

        bp = ClientUserPermission.objects.create(
            auth=ClientUserAuthentication.objects.get(auth_token=auth_token),
            permission_type=ClientUserPermission.PERMISSIONS.VIEW
        )
        bp.save()

        print(json.loads(RequestAssertion(self.client).update(
            url=reverse('ca-perms'),
            kwargs={
                'HTTP_X_CLIENT': str(client.pk),
                'HTTP_X_AUTH_TOKEN': auth_token,
            }
        ).execute()
         .response.content.decode()) == [{'permission_type': [1, 'View']}])
