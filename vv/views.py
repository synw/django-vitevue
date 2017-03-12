# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from vv.conf import VV_APPS


class IndexView(TemplateView):
    template_name = "vv/index.html"
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        apps = {}
        for appname in VV_APPS:
            parts = {
                "routes": appname+"/routes.js",
                "data": appname+"/vues/data.js",
                "methods": appname+"/vues/methods.js",
                "computed": appname+"/vues/computed.js",
                "components": appname+"/vues/components.js"
            }
            apps[appname] = parts
        context['apps'] = apps 
        return context
