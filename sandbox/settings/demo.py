# flake8: noqa: F403
"""
Django settings for demonstration

Intended to be used with ``make run``.
"""
from sandbox.settings.base import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": join(VAR_PATH, "db", "db.sqlite3"),
    }
}
