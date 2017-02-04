from django.conf.urls import url, include

from clients.views import ClientApplicationList, ClientGenToken, ClientLogin
from clients.views import ClientPermissionsList, ClientLogout

ca_urls = [
    url(r'^$', ClientApplicationList.as_view(), name='ca-lcdapi'),
    url(r'^token/$', ClientGenToken.as_view(), name='clacsrft'),
    url(r'^login/$', ClientLogin.as_view(), name='ca-login'),
    url(r'^logout/$', ClientLogout.as_view(), name='ca-logout'),
    url(r'^perms/$', ClientPermissionsList.as_view(), name='ca-perms')
]

urlpatterns = [
    url(r'^ca/', include(ca_urls)),
]
