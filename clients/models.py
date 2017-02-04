from __future__ import unicode_literals
import uuid
import hashlib
import string
import random
from datetime import datetime

from django.db import models
from django.conf import settings

from lazy_extensions.lazyenum import LazyEnum, LazyEnumField


def generate_secret():
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(256)
    )


class ClientApplication(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    client_secret = models.CharField(max_length=256, default=generate_secret)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    # The domain, in the format https://do.main/
    domain = models.CharField(max_length=100, default="https://example.com/")

    def sign(self, data):
        return hashlib.sha512((data + self.client_secret).encode('utf-8')) \
            .hexdigest()

    def sign_request(self, request):
        shared_secret = "\0".join((
            request.path,
            request.body.decode(),
        ))
        return self.sign(shared_secret)

    def verify(self, data, signature):
        # TODO: Make this IND-CPA secure
        return self.sign(data) == signature

    def verify_request(self, request, signature):
        return self.sign_request(request) == signature


class ClientUserAuthentication(models.Model):
    client = models.ForeignKey(ClientApplication)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    auth_token = models.CharField(max_length=256, default=generate_secret)

    class Meta:
        unique_together = (('client', 'user'), )


class ClientLoginACSRFT(models.Model):
    client = models.ForeignKey(ClientApplication)
    auth_token = models.CharField(max_length=256, default=generate_secret)
    time = models.DateTimeField(default=datetime.now)

    class Meta:
        unique_together = (('client', 'auth_token'), )


class ClientUserPermission(models.Model):
    PERMISSIONS = LazyEnum("*", "View", "Create")

    auth = models.ForeignKey(ClientUserAuthentication)
    permission_type = LazyEnumField(choices=PERMISSIONS)

    class Meta:
        unique_together = (('auth', 'permission_type'),)
