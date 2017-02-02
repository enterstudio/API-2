from rest_framework.test import APITestCase
from django.contrib.auth.models import User


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
        self.kwargs = {}

    def update(self, **kwargs):
        self.__dict__.update(kwargs)
        return self

    def execute(self):
        if self.method == 'POST':
            print(self.url, "potate")
            self.response = self.client.post(self.url, self.data,
                                             format='json', **self.kwargs)
        elif self.method == 'GET':
            self.response = self.client.get(self.url, self.data, format='json',
                                            **self.kwargs)
        else:
            raise NotImplementedError
        assert self.response.status_code == self.status, \
            'Mismatch {} =/= {}'.format(self.response.status_code, self.status)
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
