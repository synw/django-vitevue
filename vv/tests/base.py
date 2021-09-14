from pathlib import Path

from django.test import TestCase
from django.conf import settings


class VvBaseTest(TestCase):
    @property
    def base_dir(self) -> Path:
        d = settings.BASE_DIR
        if isinstance(d, str):
            d = Path(d)
        return d
