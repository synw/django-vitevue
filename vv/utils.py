# -*- coding: utf-8 -*-
from django.middleware.csrf import CsrfViewMiddleware


def check_csrf(request):
    reason = CsrfViewMiddleware().process_view(request, None, (), {})
    if reason:
        return False
    return True