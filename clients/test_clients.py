from django.urls import reverse

from rest_framework import status

from lazy_extensions.lazy_api_test import LazyAPITestBase, RequestAssertion


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
