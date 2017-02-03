from django.contrib import admin
from clients.models import ClientApplication, ClientUserAuthentication
from clients.models import ClientLoginACSRFT, ClientUserPermissions

admin.site.register(ClientApplication)
admin.site.register(ClientUserAuthentication)
admin.site.register(ClientLoginACSRFT)
admin.site.register(ClientUserPermissions)
# Register your models here.
