from pathlib import Path
from typing import Dict, List

from django.conf import settings


VITE_APPS: List[Dict[str, Path]] = getattr(settings, "VITE_APPS", [])
