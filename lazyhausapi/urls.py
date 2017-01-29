from django.conf.urls import url, include
from django.contrib import admin
import api


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('api.urls'))
]
