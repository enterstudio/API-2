from django.test import TestCase
from django.contrib.auth import get_user_model

from api.models import Haus, UAC, Device, Sensor

User = get_user_model()


# These are quite possibly, the worst tests I've ever passed my
# unsuspecting eyes upon. If people thought tests were hard, they haven't
# seen someone attempt to write these.
class StringConversionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super(StringConversionTests, cls).setUpTestData()
        User.objects.create(username="user")
        Haus(name="haus", owner=User.objects.first()).save()
        UAC(haus=Haus.objects.first(), user=User.objects.first(),
            level=UAC.LEVELS.OWNER).save()
        Device(name="device", haus=Haus.objects.first()).save()
        Sensor(name="sensor", device=Device.objects.first(),
               category=Sensor.CATEGORIES.PIR).save()

    def test_haus(self):
        haus = Haus.objects.first()
        self.assertEqual(str(haus), "haus, owned by user")
        self.assertEqual(repr(haus),
                         "<Haus: {!r}, <User: user>>".format(u"haus"))

    def test_uac(self):
        uac = UAC.objects.first()
        self.assertEqual(str(uac), "Permission of user in the Haus haus, " +
                                   "owned by user: Owner")
        self.assertEqual(repr(uac),
                         ("<UAC: <User: user>, <Haus: {!r}, " +
                          "<User: user>>, <Value: {!r}, 0>>").format(u"haus",
                                                                     "Owner"))

    def test_device(self):
        device = Device.objects.first()
        self.assertEqual(str(device), "device")
        self.assertEqual(repr(device),
                         ("<Device: {!r}, <Haus: {!r}," +
                          " <User: user>>>").format(u"device", u"haus"))

    def test_sensors(self):
        sensor = Sensor.objects.first()
        self.assertEqual(str(sensor), "sensor")
        self.assertEqual(repr(sensor),
                         ("<Sensor: {!r}, <Device: {!r}," +
                         " <Haus: {!r}, <User: user>>>>").format(u"sensor",
                                                                 u"device",
                                                                 u"haus"))
        self.assertEqual(sensor.category, ("PIR", 2))
