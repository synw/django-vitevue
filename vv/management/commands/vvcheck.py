from django.core.management.base import BaseCommand

from introspection.colors import colors
from vv.conf import VvConfManager


class Command(BaseCommand):
    help = "Check your vv config and settings"

    def add_arguments(self, parser):
        parser.add_argument(
            "-i",
            action="store_true",
            dest="info",
            default=False,
            help="Display info about the settings found",
        )

    def handle(self, *args, **options):
        conf = VvConfManager()
        issues = conf.check_vv_settings(options["info"])
        if len(issues) > 0:
            print(f"Found {len(issues)} issues:")
            for issue in issues:
                print(colors.red("required"), issue)
        else:
            print(colors.green("ok"), "no issues found")
