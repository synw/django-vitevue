from pathlib import Path
from typing import Dict, List
from vv.conf.models import VVAppConf

from django.conf import settings
from django.core.management.base import BaseCommand

from vv.conf import VvConfManager
from vv.configure import (
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
        # get the settings
        manager = VvConfManager()
        print("Reading VITE_APPS config in settings ..")
        apps: List[VVAppConf] = []
        if options["app"] is not None:
            # print(f'Generating config for app {options["app"]}')
            app_path = manager.conf.vv_base_dir / options["app"]
            if not app_path.exists():
                raise ValueError(
                    (
                        f'The folder {options["app"]} does not exist in'
                        f"{manager.conf.base_dir}"
                    )
                )
            app_conf = manager.frontend_app_conf(app_path)
            apps.append(app_conf)
        elif manager.has_conf is False:
            print(
                "No VITE_APPS config found, searching for default a frontend folder..."
            )
            # check if a directory named "frontend" exists
            path = Path(manager.conf.vv_base_dir / "frontend")
            if path.exists():
                apps.append(manager.frontend_app_conf(path))
            else:
                print(
                    (
                        "No frontend folder found, you might create one in "
                        f"{manager.conf.base_dir} with a Vite command like:"
                    )
                )
                print("yarn create vite frontend --template=vue-ts")
        else:
            apps = list(manager.conf.apps.values())
        # compile apps
        for app in apps:
            viteconf = generate_vite_compilation_config(manager.conf, app)
            packages_cmds: Dict[str, str] = generate_packages_json_build_commands(
                manager.conf, app
            )
            packages_file = app.directory / "package.json"
            dev_deps: Dict[str, str] = {}
            if options["write"] is True:
                write_conf(app.directory, viteconf)
                print("Writing package.json")
                _, dev_deps = packages_conf(packages_file, packages_cmds)
            else:
                print("-----------------------------------")
                print(f"Config for app {app.directory.name}")
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
