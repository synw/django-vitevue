from pathlib import Path
import re
import os
from typing import Dict, Tuple, Union

from django.conf import settings

from introspection.const import NUMBER_FIELDS, STRING_FIELDS


def frontend_app_path(base_dir: Path, path: Union[Path, None]) -> Path:
    """
    Get a frontend app path
    """
    app_path: Union[Path, None] = None
    if path is not None:
        app_path = base_dir / path
    else:
        # try to find a default dir
        d = base_dir / "frontend"
        if d.exists():
            app_path = d
    if app_path is not None:
        if app_path.exists():
            return app_path
    if path is not None:
        raise FileNotFoundError(f"frontend app path {app_path} not found")
    else:
        raise FileNotFoundError("default frontend dir not found")


def read_conf_path(vv_base_path: Path, path: Union[str, Path]) -> Path:
    """
    Get a path from a VITE_APPS config param
    """
    if isinstance(path, str):
        return Path(vv_base_path / path)
    return path


def read_vite_app_conf(
    vv_base_path: Path, app_conf: Dict[str, Union[str, Path]]
) -> Dict[str, Path]:
    """
    Read a VITE_APPS app conf and convert to paths
    """
    conf: Dict[str, Path] = {}
    for app in app_conf:
        conf[app] = read_conf_path(vv_base_path, app_conf[app])
    return conf


def read_vite_apps_conf(
    vv_base_path: Path,
) -> Tuple[bool, Dict[str, Dict[str, Path]]]:
    """
    Read the VITE_APPS setting and get the config as paths
    """
    appconf: Dict[str, Dict[str, Path]] = {}
    if hasattr(settings, "VITE_APPS") is False:
        return False, appconf
    for app in settings.VITE_APPS:
        c = read_vite_app_conf(vv_base_path, app)
        appconf[c["dir"].name] = c
    return True, appconf


def rel_path(path: Path, relative_to: Path) -> Path:
    """
    Return a directory relative path to another directory
    """
    return Path(os.path.relpath(path, relative_to))


def to_snake_case(word: str) -> str:
    """
    Convert a string to snake case
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", word).lower()


def to_camel_case_var(word: str) -> str:
    """
    Convert a string to camel case
    """
    s = "".join(x.capitalize() or "_" for x in word.split("_"))
    return s[0].lower() + s[1:]


def field_ts_type_from_classname(classname: str):
    """
    Get a field typescript type
    """
    if classname in NUMBER_FIELDS:
        return "number"
    elif classname in STRING_FIELDS:
        return "string"
    elif classname == "JSONField":
        return "Record<string, any>"
    elif classname == "BooleanField":
        return "boolean"
    raise KeyError(f"Type for field {classname} not found")
