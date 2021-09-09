from pathlib import Path
from typing import Dict, List

from django.conf import settings
from django.core.management.base import BaseCommand

from vv.conf import VITE_APPS, read_settings
from vv.configure import (
    app_dirs,
    check_packages_dependencies,
    generate_vite_compilation_config,
    write_conf,
    generate_packages_json_build_commands,
    packages_conf,
)


class Command(BaseCommand):
    help = "Configure Vitejs to compile to Django static files and template"

    def add_arguments(self, parser):
        parser.add_argument(
            "-w",
            action="store_true",
            dest="write",
            default=False,
            help="Write to the Vite config files, print the config if not set",
        )
        parser.add_argument(
            "app",
            type=str,
            nargs="?",
            default=None,
            help="Generate a config for the specified folder, ignoring settings if set",
        )

    def handle(self, *args, **options):
        # verbosity = options["verbosity"]
        if settings.DEBUG is False:
            print("This command only works in debug mode: do not use in production")
            return
        BASE_DIR, STATICFILES_DIR, TEMPLATES_DIR = read_settings()
        # TODO : make sure that static_dir and templates_dir really exist
        # read conf from settings or try to find a default frontend dir
        print("Reading VITE_APPS config in settings ..")
        apps: List[Dict[str, Path]] = []
        if options["app"] is not None:
            # print(f'Generating config for app {options["app"]}')
            app_path = BASE_DIR / options["app"]
            if not app_path.exists():
                raise ValueError(
                    f'The folder {options["app"]} does not exist in {BASE_DIR}'
                )
            apps.append(
                {
                    "dir": app_path,
                    "template": TEMPLATES_DIR / "index.html",
                    "static": STATICFILES_DIR / "frontend",
                }
            )
        elif len(VITE_APPS) == 0:
            print("No VITE_APPS config found, searching for a frontend folder")
            # check if a directory named "frontend" exists
            if Path(BASE_DIR / "frontend").exists():
                apps.append(
                    {
                        "dir": BASE_DIR / "frontend",
                        "template": TEMPLATES_DIR / "index.html",
                        "static": STATICFILES_DIR / "frontend",
                    }
                )
        else:
            apps = VITE_APPS
        # compile apps
        static_url = settings.STATIC_URL
        for app in apps:
            viteconf = generate_vite_compilation_config(
                app["dir"], app["template"], app["static"]
            )
            rel_app_dir, rel_static_dir, rel_template = app_dirs(
                app["dir"], app["static"], app["template"]
            )
            packages_cmds: Dict[str, str] = generate_packages_json_build_commands(
                rel_app_dir, rel_static_dir, rel_template, static_url
            )
            packages_file = app["dir"] / "package.json"
            dev_deps: Dict[str, str] = {}
            if options["write"] is True:
                write_conf(app["dir"], viteconf)
                print("Writing package.json")
                _, dev_deps = packages_conf(packages_file, packages_cmds)
            else:
                print("-----------------------------------")
                print(f'Config for app {app["dir"].name}')
                print("-----------------------------------")
                print(viteconf)
                print("---- packages.json build commands ----")
                for cmd_line in packages_cmds:
                    print(f"{cmd_line} : {packages_cmds[cmd_line]}")
                _, dev_deps = packages_conf(
                    packages_file, packages_cmds, read_only=True
                )
            # checking dev dependencies
            check_packages_dependencies(dev_deps)
