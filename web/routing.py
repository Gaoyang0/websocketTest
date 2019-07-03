# -*- coding:utf-8 -*-
# Author:DaoYang


from django.conf.urls import url

from . import consumers


websocket_urlpatterns = [
    url(r'^websocket/test/(?P<user>[^/]+)/', consumers.Consumer),
]