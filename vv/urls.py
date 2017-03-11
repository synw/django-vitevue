# -*- coding: utf-8 -*-

from django.conf.urls import url
from vv.views import IndexView


urlpatterns = [url(r'^', IndexView.as_view(), name="vv-index")]
