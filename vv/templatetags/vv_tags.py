# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from vv.conf import DEBUG


register = template.Library()

@register.filter
def is_installed(vvapp):
    if vvapp in settings.INSTALLED_APPS:
        return True
    return False

@register.simple_tag
def isdebug():
    print "Debug *************************"+str(DEBUG)
    return DEBUG
