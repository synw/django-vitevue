# -*- coding: utf-8 -*-
import json
from goerr import Err
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.http import JsonResponse
from django.utils.html import escape
from vv.utils import check_csrf


class IndexView(TemplateView):
    template_name = "vv/index.html"


class PostFormView(FormView, Err):

    def action(self, request, clean_data):
        pass

    def post(self, request, *args, **kwargs):
        try:
            super(PostFormView, self).post(request, *args, **kwargs)
        except:
            pass
        if check_csrf(request) == False:
            return JsonResponse({"error": 1})
        data = json.loads(self.request.body.decode('utf-8'))
        clean_data = {}
        for field in data:
            if field != "csrfmiddlewaretoken":
                clean_data[field] = escape(data[field])
        data, err = self.action(self.request, clean_data)
        if err is None:
            resp = {"error": 0}
        else:
            resp = {"error": err}
        if data is not None:
            resp["data"] = data
        return JsonResponse(resp)
