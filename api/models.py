from django.db import models
from django.conf import settings

# Create your models here.
class Haus(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owned_hauses")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="UAC")

class Levels(object):
    _levels = ["Owner", "Admin", "Resident", "Landlord", "Guest"]

    def __init__(self, number, *args, **kwargs):
        super(Levels, self).__init__(*args, **kwargs)
        self.number = number

    def __str__(self):
        return Levels._levels[self.number]


class UAC(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    haus = models.ForeignKey(Haus)
    level = models.PositiveSmallIntegerField(choices=((i, str(Levels(i))) for i in range(5)))

for i, name in enumerate(Levels._levels):
    setattr(UAC, name.upper(), Levels(i))
