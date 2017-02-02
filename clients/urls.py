from django.conf.urls import url, include

from clients.views import ClientApplicationList

ca_urls = [
    url(r'^$', ClientApplicationList.as_view(), name='ca-lcdapi'),
]

urlpatterns = [
    url(r'^ca/', include(ca_urls)),
]
