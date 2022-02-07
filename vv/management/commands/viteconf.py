from pathlib import Path
from typing import Dict

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from introspection.colors import colors

from vv.conf import VvConfManager
from vv.conf.models import VVAppConf
from vv.configure import (
    check_packages_dependencies,
    generate_packages_json_build_commands,
    generate_vite_compilation_config,
    packages_conf,
    write_conf,
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
        # print(manager.conf.vv_base_dir, options["frontend_app_dir"])
        app: VVAppConf
        if options["frontend_app_dir"] is not None:
            # print(f'Generating config for app {options["app"]}')
            app_path = manager.conf.vv_base_dir / options["frontend_app_dir"]
            if not app_path.exists():
                raise ValueError(
                    (
                        f'The folder {options["frontend_app_dir"]} does not exist in'
                        f"{manager.conf.vv_base_dir}"
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
            app = app_conf
        else:
            print(
                "No frontend app dir given, searching for default a frontend folder..."
            )
            # check if a directory named "frontend" exists
            app_path = manager.conf.vv_base_dir / "frontend"
            if not app_path.exists():
                raise CommandError("No frontend directory found")
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
        # print(f"App {app.directory.name} conf:", app)
        missing_template = False
        partial_template_front: Path
        if options["is_partial"] is True:
            # verify the existence of the partial template in the frontend app
            partial_template_relative = app.template.relative_to(
                manager.conf.templates_dir
            )
            partial_template_front = app.directory / partial_template_relative
            if partial_template_front.exists() is False:
                missing_template = True
        # generate conf
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
            _, dev_deps = packages_conf(packages_file, packages_cmds, read_only=True)
        # checking dev dependencies
        check_packages_dependencies(dev_deps)
        # print warnings
        if missing_template is True:
            warn_msg = (
                f"The {partial_template_front} file does not exist and "  # type: ignore
                "is required for compilation of partial template."
            )
            print(colors.yellow("warning"), warn_msg)
            resp = input(
                (
                    f"Create the {partial_template_front} "  # type: ignore
                    "template? [Y/n)"
                )
            )
            create = False
            if resp in ["", "Y", "y", "yes"]:
                create = True
            if create is False:
                msg = (
                    "You can create it with this content:\n"
                    '<div id="app"></div>\n'
                    '<script type="module" src="/src/main.ts"></script>'
                )
                print(msg)
                return
            else:
                with open(partial_template_front, "x") as f:  # type: ignore
                    content = (
                        '<div id="app"></div>\n'
                        '<script type="module" src="/src/main.ts"></script>'
                    )
                    f.write(content)
                    print(
                        colors.green("ok"),
                        f"{partial_template_front} written",  # type: ignore
                    )
