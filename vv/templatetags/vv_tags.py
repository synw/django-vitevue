# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from vv.conf import VV_APPS


register = template.Library()

@register.filter
def is_installed(vvapp):
    if vvapp in settings.INSTALLED_APPS:
        return True
    return False

@register.simple_tag
def isdebug():
    debug = getattr(settings, 'VV_DEBUG', False)
    if debug is True:
        return "true"
    return "false"

@register.simple_tag
def getVvapps():        
    apps = {}
    for appname in VV_APPS:
        parts = {
            "routes": appname+"/routes.js",
            "data": appname+"/vues/data.js",
            "methods": appname+"/vues/methods.js",
            "computed": appname+"/vues/computed.js",
            "extra": appname+"/vues/extra.js",
        }
        apps[appname] = parts
    return apps 
