# -*- coding: utf-8 -*-

from django.conf import settings


DEBUG = getattr(settings, 'VV_DEBUG', False)

default_apps = ["vvpages", "vvcontact", "vvcatalog", "vvallauth"]
VV_APPS = []
for app in default_apps:
    if app in settings.INSTALLED_APPS:
        VV_APPS.append(app)
extra = getattr(settings, 'VV_APPS', [])
if len(extra) > 0:
    for el in extra:
        VV_APPS.append(el)