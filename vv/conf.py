from pathlib import Path
from typing import Dict, List, Tuple

from django.conf import settings


VITE_APPS: List[Dict[str, Path]] = getattr(settings, "VITE_APPS", [])


def read_settings() -> Tuple[Path, Path, Path]:
    """
    Check if the required settings are there and get them
    as Path
    """
    base_dir: Path
    statifiles_dir: Path
    templates_dir: Path
    # make sure all the required settings are there
    if not hasattr(settings, "BASE_DIR"):
        raise ValueError("Missing BASE_DIR setting")
    # static
    if not hasattr(settings, "STATICFILES_DIRS"):
        raise ValueError("Missing STATICFILES_DIRS setting")
    if not hasattr(settings, "STATICFILES_DIRS"):
        raise ValueError("Missing STATIC_URL setting")
    else:
        if len(settings.STATICFILES_DIRS) == 0:
            raise ValueError("STATICFILES_DIRS setting is empty")
    # templates
    if not hasattr(settings, "TEMPLATES"):
        raise ValueError("Missing TEMPLATES setting")
    else:
        if len(settings.TEMPLATES) == 0:
            raise ValueError("Empty TEMPLATES setting")
        if "DIRS" not in settings.TEMPLATES[0]:
            raise ValueError('Missing TEMPLATES["DIRS"] setting')
        if len(settings.TEMPLATES[0]["DIRS"]) == 0:
            raise ValueError('TEMPLATES["DIRS"] setting is empty')
    # get the settings and make sure they are paths
    if isinstance(settings.BASE_DIR, str):
        base_dir = Path(settings.BASE_DIR)
    else:
        base_dir = settings.BASE_DIR
    if isinstance(settings.STATICFILES_DIRS[0], str):
        statifiles_dir = Path(settings.STATICFILES_DIRS[0])
    else:
        statifiles_dir = settings.STATICFILES_DIRS[0]
    if isinstance(settings.TEMPLATES[0]["DIRS"][0], str):
        templates_dir = Path(settings.TEMPLATES[0]["DIRS"][0])
    else:
        templates_dir = settings.TEMPLATES[0]["DIRS"][0]
    # check for a VV_BASE_DIR or set to BASE_DIR parent
    vv_base_dir: Path = getattr(settings, "VV_BASE_DIR", base_dir.parent)
    return vv_base_dir, statifiles_dir, templates_dir
