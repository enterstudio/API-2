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


class RequestAssertion(object):
    def __init__(self, client, url='/', method='GET', status=200, data={}):
        self.client = client
        self.url = url
        self.method = method
        self.status = status
        self.data = data

    def update(self, **kwargs):
        self.__dict__.update(kwargs)
        return self

    def execute(self):
        if self.method == 'POST':
            response = self.client.post(self.url, self.data, format='json')
        elif self.method == 'GET':
            response = self.client.get(self.url, self.data, format='json')
        else:
            raise NotImplementedError
        assert response.status_code == self.status, 'Status mismatch'
        return self


class LazyAPITestBase(APITestCase):

    def create_admin_and_user(self):
        admin = create_user('Bojangle', 'bojang@heav.en', 'pass', True)
        user = create_user('straycat', 'stray@cat.com', 'pass', False)
        return admin, user

    def login_user(self):
        return self.client.login(username='straycat', password='pass')

    def login_admin(self):
        return self.client.login(username='Bojangle', password='pass')


class GeneralTests(LazyAPITestBase):
    def test_create_haus(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('haus-lcdapi')
        admin, _ = self.create_admin_and_user()
        self.login_admin()

        data = {
            'name': 'TestysHaus',
            'owner': admin.id,
        }
        RequestAssertion(self.client, url, "POST",
                         status.HTTP_201_CREATED, data).execute()

        self.assertEqual(Haus.objects.count(), 1)
        self.assertEqual(Haus.objects.get().name, 'TestysHaus')
        return Haus.objects.get().id


class PermissionTests(LazyAPITestBase):
    def test_lcdapi_admin_only(self):
        admin, _ = self.create_admin_and_user()

        self.login_admin()
        urls = [reverse(x + "-lcdapi")
                for x in ["haus", "sensor", "device", "uac"]]

        ra = RequestAssertion(self.client, method="GET", status=200)
        for url in urls:
            ra.update(url=url).execute()
        self.login_user()
        ra.update(status=status.HTTP_403_FORBIDDEN)
        for url in urls:
            ra.update(url=url).execute()

    def test_haus_permissions(self):
        admin, user = self.create_admin_and_user()

        haus = Haus.objects.create_haus(name="Bojangle's Crib", owner=admin)
        url = reverse('haus-detail', args=[haus.id])

        self.login_user()
        ra = RequestAssertion(self.client, url=url, method="GET",
                              status=status.HTTP_403_FORBIDDEN).execute()
        UAC.objects.create_uac(user, haus, 0)
        ra.update(status=status.HTTP_200_OK).execute()

        return admin, haus

    def test_device_permissions(self):
        # This one may require rewriting later
        admin, haus = self.test_haus_permissions()
        superd = Device.objects.create_device(name="SuperDevice", haus=haus)
        empty = Haus.objects.create_haus(name="Empty Crib", owner=admin)
        nohausd = Device.objects.create_device(name="NoHausDevice", haus=empty)

        ra = RequestAssertion(self.client).update(
            url=reverse('device-detail', args=[superd.uuid]), status=200
        ).execute().update(
            url=reverse('device-by-haus', args=[haus.id]), status=200
        ).execute().update(
            url=reverse('device-by-haus', args=[empty.id]), status=403
        ).execute().update(
            url=reverse('device-detail', args=[nohausd.uuid]), status=403
        ).execute()

        return superd, nohausd

    def test_sensor_permissions(self):
        superd, nohausd = self.test_device_permissions()
        sensor = Sensor.objects.create_sensor(superd, "1", 0)
        sensor_403 = Sensor.objects.create_sensor(nohausd, "2", 0)

        ra = RequestAssertion(self.client).update(
            url=reverse('sensor-detail', args=[sensor.id]), status=200
        ).execute().update(
            url=reverse('sensor-by-device', args=[superd.uuid]), status=200
        ).execute().update(
            url=reverse('sensor-by-device', args=[nohausd.uuid]), status=403
        ).execute().update(
            url=reverse('sensor-detail', args=[sensor_403.id]), status=403
        ).execute()

    def test_the_tests(self):
        ra = RequestAssertion(self.client, status=403, method="RAIS")
        self.assertRaises(NotImplementedError, ra.execute)
