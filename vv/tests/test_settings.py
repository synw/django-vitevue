from unittest.mock import patch

from io import StringIO

from django.core.management import call_command

# from django.test import override_settings
# from django.conf import settings

from .base import VvBaseTest


class VVTestConf(VvBaseTest):

    """def test_titles(self):
    out = StringIO()
    call_command(
        "vvcheck",
        stdout=out,
        stderr=out,
    )
    print("CMD", out.getvalue())"""

    @patch("builtins.print")
    def test_base_settings(self, mock_print):
        out = StringIO()
        call_command(
            "vvcheck",
            stdout=out,
            stderr=out,
        )
        msg = ("\x1b[92mok\x1b[0m", "no issues found")
        mock_print.assert_called_with(*msg)

    """@patch("builtins.print")
    @override_settings()
    def test_base_settings_with_issue(self, mock_print):
        # TODO: find out how to test with a setting removed
        # with self.settings(STATICFILES_DIR=None):
        del settings.STATICFILES_DIR  # type: ignore
        out = StringIO()
        call_command(
            "vvcheck",
            stdout=out,
            stderr=out,
        )
        msg = "found 1 issues"
        mock_print.assert_called_with(*msg)"""
