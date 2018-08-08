# -*- coding: utf-8 -*-
import json
from goerr import Err
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.utils.html import escape
from vv.utils import check_csrf


class IndexView(TemplateView):
    template_name = "vv/index.html"


class PostFormView(CreateView, Err):
    model = None
    fields = []

    def action(self, request, clean_data):
        pass

    def post(self, request, *args, **kwargs):
        if check_csrf(request) == False:
            return JsonResponse({"error": 1})
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            clean_data = {}
            for field in self.fields:
                clean_data[field] = escape(data[field])
            data = self.action(self.request, clean_data)
            resp = {"error": 0}
            if data is not None:
                resp = {"error": 0, **data}
            return JsonResponse(resp)
        except Exception as e:
            err = self.err(e)
            return JsonResponse({"error": err.msg})
