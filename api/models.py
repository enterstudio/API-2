import string
import random

import uuid

from django.db import models
from django.conf import settings

from lazy_extensions.lazyenum import LazyEnum, LazyEnumField
from lazy_extensions.models import LazySigner


class HausManager(models.Manager):
    def create_haus(self, name, owner):
        haus = self.create(name=name, owner=owner)
        return haus


class Haus(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name="owned_hauses")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="UAC")

    objects = HausManager()

    def __str__(self):
        return "{0.name}, owned by {0.owner!s}".format(self)

    def __repr__(self):
        return "<Haus: {0.name!r}, {0.owner!r}>".format(self)

    class Meta:
        verbose_name_plural = u"H\xe4user"


class UACManager(models.Manager):
    def create_uac(self, user, haus, level=4):
        uac = self.create(user=user, haus=haus, level=level)
        return uac


class UAC(models.Model):
    LEVELS = LazyEnum("Owner", "Admin", "Resident", "Landlord", "Guest")

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    haus = models.ForeignKey(Haus)
    level = LazyEnumField(choices=LEVELS)

    objects = UACManager()

    def __str__(self):
        return ("Permission of {0.user!s} in the Haus {0.haus!s}:" +
                " {0.level!s}").format(self)

    def __repr__(self):
        return "<UAC: {0.user!r}, {0.haus!r}, {0.level!r}>".format(self)

    class Meta:
        verbose_name = "User Access Control"
        unique_together = (('user', 'haus', ), )


class DeviceManager(models.Manager):
    def create_device(self, name, haus=None, last_ping=None):
        secret = ''.join(random.choice(string.ascii_uppercase + string.digits)
                         for _ in range(256))
        device = self.create(name=name, haus=haus, last_ping=last_ping,
                             setup_secret=secret)
        return device


class Device(LazySigner, models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False,
                            default=uuid.uuid4)
    name = models.CharField(max_length=200)
    last_ping = models.DateTimeField(db_index=True, blank=True, null=True)
    haus = models.ForeignKey(Haus, blank=True, null=True)
    setup_secret = models.CharField(max_length=256)

    objects = DeviceManager()

    def lazy_secret(self):
        return self.setup_secret

    def __str__(self):
        return "{0.name}".format(self)

    def __repr__(self):
        return "<Device: {0.name!r}, {0.haus!r}>".format(self)


class SensorManager(models.Manager):
    def create_sensor(self, devic, name, category, last_datum=0, formatter=''):
        sensor = self.create(device=devic, name=name, category=category,
                             last_datum=last_datum, formatter=formatter)
        # TODO filestore
        return sensor


class Sensor(models.Model):
    CATEGORIES = LazyEnum(
        "Other",
        "Temperature",
        "PIR",
        "Gyroscope",
        "Moisture",
        "Light",
        "Smoke",
        "Molecule Detector",
        "Radiation",
    )
    device = models.ForeignKey(Device)
    name = models.CharField(max_length=200)
    category = LazyEnumField(choices=CATEGORIES)
    last_datum = models.TextField()
    formatter = models.TextField()
    file_store = models.FileField(blank=True, null=True)

    objects = SensorManager()

    def __str__(self):
        return "{0.name}".format(self)

    def __repr__(self):
        return "<Sensor: {0.name!r}, {0.device!r}>".format(self)
