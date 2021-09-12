import os
from pathlib import Path
from shutil import copy

from django.conf import settings
from django.core.management.base import BaseCommand
from introspection.inspector.inspector import AppInspector

from vv import files
from vv.conf import read_settings
from vv.frontend_models.model import FrontendModel
from vv.utils import frontend_app_path


class Command(BaseCommand):
    help = "Create a Typescript api for existing models"

    def add_arguments(self, parser):
        parser.add_argument(
            "app",
            nargs="+",
            type=str,
            help="the Django app name to generate api models for",
        )
        parser.add_argument(
            "-w",
            nargs="?",
            dest="frontend_dir",
            type=str,
            default=None,
            help="the frontend folder to add api to models",
        )

    def handle(self, *args, **options):
        # verbosity = options["verbosity"]
        if settings.DEBUG is False:
            print("This command only works in debug mode: do not use in production")
            return
        VV_BASE_DIR, _, _ = read_settings()
        app_path = frontend_app_path(VV_BASE_DIR, options["frontend_dir"]) / "src"
        print("App path:", app_path)
        files_path = Path(os.path.dirname(files.__file__))
        print("Mod", files_path)
        api_path = app_path / "api"
        rel_app_path = app_path.relative_to(VV_BASE_DIR)
        if api_path.exists() is True:
            print(
                (
                    f"The api directory already exists in {rel_app_path}, skipping api "
                    "files copy"
                )
            )
        else:
            print(f"Creating directory {api_path.relative_to(VV_BASE_DIR)}")
            os.mkdir(api_path)
            print(f"Adding api files in {rel_app_path} ...")
            copy(files_path / "api/model.ts", api_path)
            copy(files_path / "api/interface.ts", api_path)
            copy(files_path / "api/index.ts", api_path)
        # check dirs
        models_dir = app_path / "models"
        if models_dir.exists() is False:
            raise FileNotFoundError(f"No models directory in {app_path}")
        print("Adding api file ...")
        app_name = options["app"][0]
        app = AppInspector(app_name)
        app.get_models()
        for mod in app.models:
            model = FrontendModel(mod)
            folder_path = models_dir / f"{model.snake_case_name}"
            print(f"Updating model in {folder_path}")
            filename = f"{folder_path}/index.ts"
            # print(f"Writing config in {filename.name}")
            lines = open(filename, "r").readlines()
            lines[0] = model.api_relative_import + ";\n" + lines[0]
            new_last_line = (
                lines[-1].rstrip().replace("}", f"\n{model.load_method()}\n" + "}")
            )
            lines[-1] = new_last_line
            open(filename, "w").writelines(lines)
