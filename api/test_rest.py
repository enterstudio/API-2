from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Haus, Device, UAC, Sensor


def create_user(username, email, pw, is_staff):
    user = User.objects.create_user(username, email, pw)
    user.is_staff = is_staff
    user.save()
    return user


def create_haus(name, owner):
    haus = Haus.objects.create_haus(name=name, owner=owner)
    return haus


def assert_get(obj, urls, assert_status):
    for url in urls:
        response = obj.client.get(url, {}, format='json')
        obj.assertEqual(response.status_code, assert_status)


def create_admin_and_user():
    admin = create_user('Bojangle', 'bojang@heav.en', 'pass', True)
    user = create_user('straycat', 'stray@cat.com', 'pass', False)
    return admin, user


class GeneralTests(APITestCase):
    def test_create_haus(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('haus-lcdapi')
        admin = create_user('god', 'got@heav.en', 'pass', True)
        data = {
            'name': 'TestysHaus',
            'owner': admin.id,
        }
        self.client.login(username='god', password='pass')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Haus.objects.count(), 1)
        self.assertEqual(Haus.objects.get().name, 'TestysHaus')
        return Haus.objects.get().id


class PermissionTests(APITestCase):
    def test_lcdapi_admin_only(self):
        admin, user = create_admin_and_user()

        self.client.login(username='Bojangle', password='pass')
        lcdapi_urls = [reverse(x + "-lcdapi")
                       for x in ["haus", "sensor", "device", "uac"]]
        assert_get(self, lcdapi_urls, status.HTTP_200_OK)
        self.client.login(username='straycat', password='pass')
        assert_get(self, lcdapi_urls, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_haus_permissions(self):
        admin, user = create_admin_and_user()

        haus = create_haus("Bojangle's Crib", admin)
        url = reverse('haus-detail', args=[haus.id])

        self.client.login(username='straycat', password='pass')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        UAC.objects.create_uac(user=user, haus=haus, level=0).save()

        # Now user should have permission to view the haus
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()
