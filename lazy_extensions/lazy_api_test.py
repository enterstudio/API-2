from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from django.contrib.auth import authenticate

from clients.models import ClientUserAuthentication


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

    def make_kwargs(self, base, update):
        new_dict = base.copy()
        new_dict.update(update)
        return new_dict

    def execute(self):
        if self.method == 'POST':
            self.response = self.client.post(
                self.url, self.data, format='json',
                **self.make_kwargs(self.kwargs, self.client.lazy_auth)
            )
        elif self.method == 'GET':
            self.response = self.client.get(
                self.url, self.data, format='json',
                **self.make_kwargs(self.kwargs, self.client.lazy_auth)
            )
        else:
            raise NotImplementedError
        assert self.response.status_code == self.status, \
            'Mismatch {} =/= {}'.format(self.response.status_code, self.status)
        return self


class LazyAPITestBase(APITestCase):

    def setUp(self):
        self.client.lazy_auth = {}

    def create_admin_and_user(self):
        admin = create_user('Bojangle', 'bojang@heav.en', 'pass', True)
        user = create_user('straycat', 'stray@cat.com', 'pass', False)
        return admin, user

    def login(self, client_app, username, password):
        u = authenticate(username=username, password=password)
        if u is not None:
            uac, _ = ClientUserAuthentication.objects.get_or_create(
                user=u,
                client=client_app
            )
            uac.save()
            self.client.lazy_auth = {
                'HTTP_X_CLIENT': str(client_app.pk),
                'HTTP_X_AUTH_TOKEN': uac.auth_token,
            }
        return u

    def login_user(self, client_app):
        return self.login(client_app, 'straycat', 'pass')

    def login_admin(self, client_app):
        return self.login(client_app, 'Bojangle', 'pass')
