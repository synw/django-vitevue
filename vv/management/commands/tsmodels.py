# import os

from django.core.management.base import BaseCommand
from django.conf import settings

from introspection import AppInspector

from ...frontend_models.model import FrontendModel


class Command(BaseCommand):
    help = "Create frontend models for an app"

    def add_arguments(self, parser):
        parser.add_argument(
            "app", nargs="+", type=str, help="app name to generate models from"
        )
        parser.add_argument(
            "destination", nargs="+", type=str, help="compilation destination"
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
        print(f"Creating frontend models for app {app_name}")
        app = AppInspector(app_name)
        app.get_models()
        for model in app.models:
            print(f"Creating frontend model {model.name}")
            fm = FrontendModel(model)
            print(fm.tsclass())
            print("------------")
            print(fm.interface())
            print(options["destination"][0])
            # if not os.path.exists("/tmp/test"):
            #    with open("/tmp/test", "w"):
            #        pass
