from django.conf.urls import url, include

from clients.views import ClientApplicationList, ClientGenToken, ClientLogin

ca_urls = [
    url(r'^$', ClientApplicationList.as_view(), name='ca-lcdapi'),
    url(r'^token/$', ClientGenToken.as_view(), name='clacsrft'),
    url(r'^ca_login/$', ClientLogin.as_view(), name='ca-login')
]

urlpatterns = [
    url(r'^ca/', include(ca_urls)),
]
