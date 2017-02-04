from django.contrib import admin
from clients.models import ClientApplication, ClientUserAuthentication
from clients.models import ClientLoginACSRFT, ClientUserPermission

admin.site.register(ClientApplication)
admin.site.register(ClientUserAuthentication)
admin.site.register(ClientLoginACSRFT)
admin.site.register(ClientUserPermission)
# Register your models here.
