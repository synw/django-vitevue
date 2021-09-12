import os

from django.core.management.base import BaseCommand
from django.conf import settings

from introspection import AppInspector
from introspection.inspector import title, subtitle

from vv.conf import read_settings
from vv.frontend_models.model import FrontendModel
from vv.frontend_models.write import write_tsmodel
from vv.utils import frontend_app_path


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
            "-w",
            nargs="?",
            dest="destination",
            type=str,
            default=None,
            help="the frontend app to add models to. A models directory "
            "will be created into it if it does not exists",
        )

    def handle(self, *args, **options):
        # verbosity = options["verbosity"]
        if settings.DEBUG is False:
            print("This command only works in debug mode: do not use in production")
            return
        if "app" not in options:
            print("Provide an app to generate models for")
            return
        app_name = options["app"][0]
        app = AppInspector(app_name)
        app.get_models()
        for model in app.models:
            title(f"Model {model.name}")
            fm = FrontendModel(model)
            if options["destination"] is None:
                print(fm.tsclass() + "\n")
                subtitle("Interface")
                print("\n" + fm.interface())
            else:
                VV_BASE_DIR, _, _ = read_settings()
                app_src = frontend_app_path(VV_BASE_DIR, options["destination"]) / "src"
                models_dir = app_src / "models"
                if not models_dir.exists():
                    print("Creating models directory")
                    os.mkdir(models_dir)
                name = fm.snake_case_name
                dest_dir = models_dir / name
                if not dest_dir.exists():
                    print(f"Creating directory {name}")
                    os.mkdir(dest_dir)
                write_tsmodel(fm, dest_dir)
