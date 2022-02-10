import os
from pathlib import Path
from shutil import copy

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from introspection.inspector.inspector import AppInspector

from vv import files
from vv.conf.manager import VvConfManager
from vv.conf.models import VVAppConf
from vv.frontend_models.model import FrontendModel


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
            "--app",
            nargs="?",
            dest="frontend_app_dir",
            type=str,
            default=None,
            help="the frontend app models to add api to. An api directory "
            "will be created",
        )

    def handle(self, *args, **options):
        # verbosity = options["verbosity"]
        if settings.DEBUG is False:
            print("This command only works in debug mode: do not use in production")
            return
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
        files_path = Path(os.path.dirname(files.__file__))
        api_path = app_conf.directory / "src/api"
        rel_src_path = (app_conf.directory / "src").relative_to(
            manager.conf.vv_base_dir
        )
        if api_path.exists() is True:
            print(
                (
                    f"The api directory already exists in {rel_src_path}, skipping api "
                    "files copy"
                )
            )
        else:
            print(
                f"Creating directory {api_path.relative_to(manager.conf.vv_base_dir)}"
            )
            os.mkdir(api_path)
            print(f"Adding api files in {rel_src_path} ...")
            # copy(files_path / "api/model.ts", api_path)
            # copy(files_path / "api/interface.ts", api_path)
            copy(files_path / "api/index.ts", api_path)
            copy(files_path / "api/api.ts", api_path)
        # check dirs
        models_dir = app_conf.directory / "src/models"
        if models_dir.exists() is False:
            print(f"No models directory {models_dir} found, exiting")
            return
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
        print("Install the dependencies in the frontend:")
        print("yarn add js-cookie @snowind/api")
        print("or npm install js-cookie @snowind/api")
