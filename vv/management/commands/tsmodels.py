import os
from vv.conf.models import VVAppConf
from vv.conf.manager import VvConfManager

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from introspection import AppInspector
from introspection.inspector import title, subtitle

from vv.frontend_models.model import FrontendModel
from vv.frontend_models.write import write_tsmodel


class Command(BaseCommand):
    help = "Create Typescript models for an app"

    def add_arguments(self, parser):
        parser.add_argument(
            "app",
            nargs="+",
            type=str,
            help="the Django app name to generate models from",
        )
        parser.add_argument(
            "--app",
            nargs="?",
            dest="frontend_app_dir",
            type=str,
            default=None,
            help="the frontend app to add models to. A models directory "
            "will be created into it if it does not exists",
        )
        parser.add_argument(
            "-w",
            action="store_true",
            dest="write",
            default=False,
            help="Write to the Vite config files, print the config if not set",
        )

    def handle(self, *args, **options):
        # verbosity = options["verbosity"]
        if settings.DEBUG is False:
            print("This command only works in debug mode: do not use in production")
            return
        if "app" not in options:
            raise CommandError("Provide an app to generate models for")
        # get the settings
        app_conf: VVAppConf
        manager = VvConfManager()
        if options["frontend_app_dir"] is None:
            try:
                app_conf = manager.frontend_default_conf()
            except FileNotFoundError as e:
                raise CommandError(e)
        else:
            app_conf = manager.frontend_app_conf(options["frontend_app_dir"])
        app_name = options["app"][0]
        app = AppInspector(app_name)
        app.get_models()
        for model in app.models:
            title(f"Model {model.name}")
            fm = FrontendModel(model)
            if options["write"] is False:
                print(fm.tsclass() + "\n")
                subtitle("Interface")
                print("\n" + fm.interface())
            else:
                models_dir = app_conf.directory / "src/models"
                if not models_dir.exists():
                    print("Creating models directory")
                    os.mkdir(models_dir)
                name = fm.snake_case_name
                dest_dir = models_dir / name
                if not dest_dir.exists():
                    print(f"Creating directory {name}")
                    os.mkdir(dest_dir)
                write_tsmodel(fm, dest_dir)
