# -*- coding: utf-8 -*-
import json
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.utils.html import escape
from vv.utils import check_csrf


class IndexView(TemplateView):
    template_name = "vv/index.html"


class PostFormView(CreateView):
    model = None
    fields = []

    def action(self, request, clean_data):
        pass

    def post(self, request, *args, **kwargs):
        if check_csrf(request) == False:
            return JsonResponse({"error": 1})
        data = json.loads(self.request.body.decode('utf-8'))
        clean_data = {}
        for field in self.fields:
            clean_data[field] = escape(data[field])
        self.action(self.request, clean_data)
        return JsonResponse({"error": 0})
