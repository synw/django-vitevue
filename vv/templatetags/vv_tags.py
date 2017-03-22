# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from vv.conf import DEBUG, VV_APPS


register = template.Library()

@register.filter
def is_installed(vvapp):
    if vvapp in settings.INSTALLED_APPS:
        return True
    return False

@register.simple_tag
def isdebug():
    return DEBUG

@register.simple_tag
def getVvapps():        
    apps = {}
    for appname in VV_APPS:
        parts = {
            "routes": appname+"/routes.js",
            "data": appname+"/vues/data.js",
            "methods": appname+"/vues/methods.js",
            "computed": appname+"/vues/computed.js",
            "components": appname+"/vues/components.js",
            "extra": appname+"/vues/extra.js",
        }
        apps[appname] = parts
    return apps 
