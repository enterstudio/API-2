from django.conf.urls import url, include

from .views import HausList, HausDetail
from .views import DeviceList, DeviceDetailByUUID, DeviceListByHaus
from .views import SensorList, SensorListByDevice, SensorById
from .views import UACList, UACDetail


haus_urls = [
    url(r'^$', HausList.as_view(), name='haus-lcdapi'),
    url(r'^(?P<pk>[0-9]+)$', HausDetail.as_view(), name='haus-detail'),
    url(r'^(?P<haus>[0-9]+)/devices$', DeviceListByHaus.as_view()),
]

device_urls = [
    url(r'^$', DeviceList.as_view(), name='device-lcdapi'),
    url(r'^(?P<uuid>[a-z0-9\-]+)$', DeviceDetailByUUID.as_view()),
    url(r'^(?P<device>[a-z0-9\-]+)/sensors$', SensorListByDevice.as_view()),
]

sensor_urls = [
    url(r'^$', SensorList.as_view(), name='sensor-lcdapi'),
    url(r'^(?P<pk>[0-9\-]+)/$', SensorById.as_view()),
]

uac_urls = [
    url(r'^$', UACList.as_view(), name='uac-lcdapi'),
    url(r'^(?P<pk>[0-9]+)/$', UACDetail.as_view()),
]

urlpatterns = [
    url(r'^haus/', include(haus_urls)),
    url(r'^device/', include(device_urls)),
    url(r'^sensor/', include(sensor_urls)),
    url(r'^uac/', include(uac_urls)),
    url(r'^', include(haus_urls))
]
