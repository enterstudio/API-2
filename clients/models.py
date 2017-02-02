from __future__ import unicode_literals
import uuid
import hashlib
import string
import random

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

    def sign(self, data):
        return hashlib.sha512((data + self.client_secret).encode('utf-8')) \
            .hexdigest()

    def verify(self, data, signature):
        # TODO: Make this IND-CPA secure
        return self.sign(data) == signature


class ClientUserAuthentication(models.Model):
    client = models.ForeignKey(ClientApplication)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    auth_token = models.CharField(max_length=256)

    class Meta:
        unique_together = (('client', 'user'), )


class ClientUserPermissions(models.Model):
    PERMISSIONS = LazyEnum("Test")

    auth = models.ForeignKey(ClientUserAuthentication)
    permission_type = LazyEnumField(choices=PERMISSIONS)

    class Meta:
        unique_together = (('auth', 'permission_type'),)
