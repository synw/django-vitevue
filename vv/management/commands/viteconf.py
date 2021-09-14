from typing import Dict, List
from vv.conf.models import VVAppConf

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

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
            "--app",
            nargs="?",
            dest="frontend_app_dir",
            type=str,
            default=None,
            help="Generate a config for the specified frontend app folder",
        )
        parser.add_argument(
            "-w",
            action="store_true",
            dest="write",
            default=False,
            help="Write to the Vite config files, print the config if not set",
        )
        parser.add_argument(
            "-p",
            action="store_true",
            dest="is_partial",
            default=False,
            help="Compile to a partial template",
        )
        parser.add_argument(
            "--template",
            nargs="?",
            dest="template",
            type=str,
            default=None,
            help="The template to compile to",
        )
        parser.add_argument(
            "--static",
            type=str,
            nargs="?",
            dest="static",
            default=None,
            help="The static folder to compile to",
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
        if options["frontend_app_dir"] is not None:
            # print(f'Generating config for app {options["app"]}')
            app_path = manager.conf.vv_base_dir / options["frontend_app_dir"]
            if not app_path.exists():
                raise ValueError(
                    (
                        f'The folder {options["app"]} does not exist in'
                        f"{manager.conf.base_dir}"
                    )
                )
            static: str = app_path.name
            if options["static"] is not None:
                static = options["static"]
            template: str = "index.html"
            if options["template"] is not None:
                template = options["template"]
            else:
                if options["is_partial"] is True:
                    template = app_path.name + ".html"
            app_conf = manager.frontend_app_conf(
                app_path.name,
                template_path=template,
                static_path=static,
                is_partial=options["is_partial"],
            )
            apps.append(app_conf)
        else:
            print(
                "No frontend app dir given, searching for default a frontend folder..."
            )
            # check if a directory named "frontend" exists
            try:

                template: str = "index.html"
                if options["template"] is not None:
                    template = options["template"]
                else:
                    if options["is_partial"] is True:
                        template = "frontend.html"
                app = manager.frontend_default_conf(
                    template_path=template, is_partial=options["is_partial"]
                )
                static: str = app.directory.name
                if options["static"] is not None:
                    static = options["static"]
                apps.append(app)
            except FileNotFoundError as e:
                raise CommandError(e)
        # compile apps
        for app in apps:
            # print(f"App {app.directory.name} conf:", app)
            viteconf = generate_vite_compilation_config(
                manager.conf, app, options["is_partial"]
            )
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
