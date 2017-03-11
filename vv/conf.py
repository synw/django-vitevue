# -*- coding: utf-8 -*-

from django.conf import settings


DEBUG = getattr(settings, 'VV_DEBUG', False)

VV_APPS = ["vvpages", "vvcontact"]
extra = getattr(settings, 'VV_APPS', [])
if len(extra) > 0:
    for el in extra:
        VV_APPS.append(el)
