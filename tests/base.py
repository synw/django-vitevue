from pathlib import Path

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.conf import settings


class VvBaseTest(TestCase):
    user = None

    def setUp(self):
        self.factory = RequestFactory()  # type: ignore
        self.user = User.objects.create_user(  # type: ignore
            "myuser", "myemail@test.com", "password"
        )
        self.superuser = User.objects.create_superuser(  # type: ignore
            "superuser", "myemail@test.com", "password"
        )

    @property
    def base_dir(self) -> Path:
        d = settings.BASE_DIR
        if isinstance(d, str):
            d = Path(d)
        return d
