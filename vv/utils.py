import os
import re
from pathlib import Path

from introspection.const import NUMBER_FIELDS, STRING_FIELDS


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
