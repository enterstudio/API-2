import string
import random

import uuid

from django.db import models
from django.conf import settings


class LazyEnum(object):
    class Value(object):
        def __init__(self, value, name, *args, **kwargs):
            super(LazyEnum.Value, self).__init__(*args, **kwargs)
            self.value = value
            self.name = name

        def __eq__(self, other):
            return other in [
                (self.value, self.name),
                (self.name, self.value),
                self.value,
                self.name,
                self.name.upper(),
            ]

        def __len__(self):
            return 2

        def __getitem__(self, key):
            return (self.value, self.name)[key]

        def __iter__(self):
            return iter((self.value, self.name))

        def __int__(self):
            return self.value

        def __str__(self):
            return self.name

        def __repr__(self):
            return "<Value: {0.name!r}, {0.value!r}>".format(self)

    def __init__(self, *values, **kwargs):
        super(LazyEnum, self).__init__(**kwargs)
        self.values = tuple(
            LazyEnum.Value(i, name) for i, name in enumerate(values)
        )
        for value in self.values:
            setattr(self, str(value).upper(), value)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __iter__(self):
        return iter(self.values)

    def from_id(self, idx):
        return self.values[idx]

    def __repr__(self):
        return "<LazyEnum: {}>".format(", ".join(repr(x) for x in self.values))


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
    def create_uac(self, user, haus):
        uac = self.create(user=user, haus=haus)
        return uac


class UAC(models.Model):
    LEVELS = LazyEnum("Owner", "Admin", "Resident", "Landlord", "Guest")

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    haus = models.ForeignKey(Haus)
    _level = models.PositiveSmallIntegerField(choices=LEVELS)

    objects = UACManager()

    @property
    def level(self):
        return UAC.LEVELS.from_id(self._level)

    def __str__(self):
        return ("Permission of {0.user!s} in the Haus {0.haus!s}:" +
                " {0.level}").format(self)

    def __repr__(self):
        return "<UAC: {0.user!r}, {0.haus!r}, {0.level!r}>".format(self)

    class Meta:
        verbose_name = "User Access Control"
        unique_together = (('user', 'haus', ), )


class DeviceManager(models.Manager):
    def create_device(self, name, haus=None, last_ping=None):
        secret = ''.join(random.choice(string.ascii_uppercase + string.digits)
                         for _ in range(N))
        device = self.create(name=name, haus=haus, last_ping=last_ping,
                             setup_secret=secret)
        return device


class Device(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False,
                            default=uuid.uuid4)
    name = models.CharField(max_length=200)
    last_ping = models.DateTimeField(db_index=True, blank=True, null=True)
    haus = models.ForeignKey(Haus, blank=True, null=True)
    setup_secret = models.CharField(max_length=256)

    objects = DeviceManager()

    def __str__(self):
        return "{0.name}".format(self)

    def __repr__(self):
        return "<Device: {0.name!r}, {0.haus!r}>".format(self)


class SensorManager(models.Manager):
    def create_sensor(self, devic, name, category, last_datum=0, formatter=''):
        sensor = self.create(device=devic, name=name, _category=category,
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
    _category = models.PositiveSmallIntegerField(choices=CATEGORIES)
    last_datum = models.TextField()
    formatter = models.TextField()
    file_store = models.FileField(blank=True, null=True)

    objects = SensorManager()

    @property
    def category(self):
        return Sensor.CATEGORIES.from_id(self._category)

    def __str__(self):
        return "{0.name}".format(self)

    def __repr__(self):
        return "<Sensor: {0.name!r}, {0.device!r}>".format(self)
