# flake8: noqa: F405,F403
"""
Django settings for tests
"""

from sandbox.settings.base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST": {
            "NAME": join(VAR_PATH, "db", "tests.sqlite3"),  # noqa
        },
    }
}

# Media directory dedicated to tests to avoid polluting other environment
# media directory
# MEDIA_ROOT = join(VAR_PATH, "media-tests")
