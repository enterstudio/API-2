from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Haus


def create_user(username, email, pw, is_staff):
    user = User.objects.create_user(username, email, pw)
    user.is_staff = is_staff
    user.save()
    return user


def create_haus(name, owner):
    haus = Haus.objects.create_haus(name=name, owner=owner)
    return haus


class HausTests(APITestCase):
    def test_create_haus(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('haus-main')
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

    def test_haus_details(self):
        idx = self.test_create_haus()
        url = reverse('haus-detail', args=[idx])
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
