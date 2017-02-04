from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import ClientApplication, ClientUserAuthentication, \
    ClientUserPermission

User = get_user_model()


class ClientModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user")
        self.user.save()
        self.application = ClientApplication(name="test",
                                             owner=self.user)
        self.application.save()

    def test_signatures(self):
        sig = self.application.sign("What is this?")
        self.assertTrue(self.application.verify("What is this?", sig))
        self.assertFalse(self.application.verify("This is not that", sig))
