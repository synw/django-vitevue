# pyright: reportUnboundVariable=false
from pathlib import Path
from typing import Dict, Set, Tuple, Union

from django.conf import settings

from vv.conf.models import VVAppConf, VVConf


class VvConfManager:
    """
    A class to manage vv config
    """

    has_conf: bool = False
    conf: VVConf

    def __init__(self) -> None:
        self.conf = self.from_settings()

    def from_settings(self) -> VVConf:
        """Get a vv app conf from settings

        :return: a vv apps conf
        :rtype: VVConf
        """
        (
            BASE_DIR,
            VV_BASE_DIR,
            STATICFILES_DIR,
            TEMPLATES_DIR,
            STATIC_URL,
        ) = self.read_settings()
        self.conf = VVConf(
            base_dir=BASE_DIR,
            vv_base_dir=VV_BASE_DIR,
            staticfiles_dir=STATICFILES_DIR,
            templates_dir=TEMPLATES_DIR,
            static_url=STATIC_URL,
        )
        if hasattr(settings, "VITE_APPS") is True:
            self.has_conf = True
            for app_conf in settings.VITE_APPS:
                ac = self.read_app_conf(app_conf)
                self.conf.apps[ac.directory.name] = ac
        return self.conf

    def frontend_app_conf(self, path: Path) -> VVAppConf:
        """Get a frontend app conf from a path. If the app exists
        in VITE_APPS return it's conf or generate a default conf
        for this path

        :param path: the path to get a conf for
        :type path: Path
        :raises FileNotFoundError: if the path does not exist
        :return: a vv app conf
        :rtype: VVAppConf
        """
        if path.exists() is False:
            raise FileNotFoundError(f"frontend app path {path} not found")
        default_app_conf: Dict[str, Path] = {
            "directory": self.conf.vv_base_dir / path.name,
            "static": self.conf.staticfiles_dir / path.name,
            "template": self.conf.templates_dir / "index.html",
        }
        app_name = path.name
        if app_name in self.conf.apps:
            return self.conf.apps[app_name]
        return VVAppConf(**default_app_conf)

    def read_app_conf(self, app_conf: Dict[str, Union[str, Path, bool]]) -> VVAppConf:
        """Read an app conf from a VITE_APPS setting

        :param app_conf: [description]
        :type app_conf: Dict[str, Union[str, Path, bool]]
        :return: [description]
        :rtype: VVAppConf
        """
        is_partial: bool = False
        params: Dict[str, Path] = {}
        for param in app_conf:
            p: Path
            if param == "is_partial":
                is_partial = bool(app_conf[param])
            else:
                if isinstance(app_conf[param], str):
                    p = Path(str(app_conf[param]))
                params[param] = p
        return VVAppConf(**params, is_partial=is_partial)

    def read_settings(self) -> Tuple[Path, Path, Path, Path, str]:
        """Check if the required settings are there and get them
        as Path

        :raises ValueError: if some required setting is not found
        :return: a tuple with base_dir, staticfiles_dir, templates_dir paths and
        a static url string
        :rtype: Tuple[Path, Path, Path, str]
        """
        base_dir: Path
        vv_base_dir: Path
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
        if hasattr(settings, "STATIC_URL") is False:
            raise ValueError("No STATIC_URL found")
        return (
            base_dir,
            vv_base_dir,
            statifiles_dir,
            templates_dir,
            str(settings.STATIC_URL),
        )

    def check_vv_settings(self, verbose: bool = False) -> Set[str]:
        """Read settings and check for issues

        :param verbose: print info, defaults to False
        :type verbose: bool, optional
        :return: a set of issues, empty if no issues is found
        :rtype: Set[str]
        """
        issues: Set[str] = set()
        if verbose is True:
            print("Checking base settings...")
        try:
            (
                BASE_DIR,
                VV_BASE_DIR,
                STATICFILES_DIR,
                TEMPLATES_DIR,
                STATIC_URL,
            ) = self.read_settings()
        except ValueError as e:
            issues.add(f"Missing setting: {e}")
        if verbose is True:
            print(f"BASE_DIR: {BASE_DIR}")
            print(f"VV_BASE_DIR: {VV_BASE_DIR}")
            print(f"STATICFILES_DIR: {STATICFILES_DIR}")
            print(f"TEMPLATES_DIR: {TEMPLATES_DIR}")
            print(f"STATIC_URL: {STATIC_URL}")
        if verbose is True:
            print("Checking the VITE_APPS setting...")
        if hasattr(settings, "VITE_APPS") is True:
            if verbose is True:
                print("Found a VITE_APPS setting:")
                print(self.from_settings().to_json_str())
        else:
            if verbose is True:
                print("No VITE_APPS setting found")
        return issues
