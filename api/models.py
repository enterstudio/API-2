from django.db import models
from django.conf import settings


class LazyEnum(object):
    class Value(object):
        def __init__(self, value, name, *args, **kwargs):
            super(LazyEnum.Value, self).__init__(*args, **kwargs)
            self.value = value
            self.name = name

        def __len__(self):
            return 2

        def __getitem__(self, key):
            return (self.value, self.name)[key]

        def __iter__(self):
            return iter((self.value, self.name))

        def __str__(self):
            return self.name

        def __repr__(self):
            return "Value({}, {})".format(self.value, self.name)

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
        return "LazyEnum({})".format(", ".join(repr(enumerate(self.values))))


# Create your models here.
class Haus(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name="owned_hauses")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="UAC")


class UAC(models.Model):
    LEVELS = LazyEnum("Owner", "Admin", "Resident", "Landlord", "Guest")

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    haus = models.ForeignKey(Haus)
    level = models.PositiveSmallIntegerField(choices=LEVELS)


class Device(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    last_ping = models.DateTimeField(db_index=True, blank=True, null=True)
    haus = models.ForeignKey(Haus, blank=True, null=True)
    setup_secret = models.CharField(max_length=256)


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
    category = models.PositiveSmallIntegerField(choices=CATEGORIES)
    last_datum = models.TextField()
    formatter = models.TextField()
    file_store = models.FileField(blank=True, null=True)
