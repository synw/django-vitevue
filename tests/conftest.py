# pyright: reportUnknownParameterType=false,reportUnknownVariableType=false
"""
Some fixture methods
"""
import os
import pytest

import vv


class ApplicationTestSettings:
    """
    Object to store settings related to application. This is almost about useful
    paths which may be used in tests. This is not related to Django settings.

    Attributes:
        application_path (str): Absolute path to the application directory.
        package_path (str): Absolute path to the package directory.
        tests_dir (str): Directory name which include tests.
        tests_path (str): Absolute path to the tests directory.
        sandbox_dir (str): Directory name of project sandbox.
        sandbox_path (str): Absolute path to the project sandbox directory.
        statics_dir (str): Directory name of sandbox static directory.
        statics_path (str): Absolute path to the sandbox static directory.
        fixtures_dir (str): Directory name which include tests datas.
        fixtures_path (str): Absolute path to the tests datas.
    """

    def __init__(self):
        self.application_path = os.path.abspath(os.path.dirname(vv.__file__))

        self.package_path = os.path.normpath(
            os.path.join(
                os.path.abspath(os.path.dirname(vv.__file__)),
                "..",
            )
        )

        self.sandbox_dir = "sandbox"
        self.sandbox_path = os.path.join(
            self.package_path,
            self.sandbox_dir,
        )

        # Sandbox static directory
        self.statics_dir = "static"
        self.statics_path = os.path.join(
            self.sandbox_path,
            self.statics_dir,
        )

        # Tests directory
        self.tests_dir = "tests"
        self.tests_path = os.path.normpath(
            os.path.join(
                os.path.abspath(os.path.dirname(vv.__file__)),
                "..",
                self.tests_dir,
            )
        )

        # Test fixtures directory
        self.fixtures_dir = "data_fixtures"
        self.fixtures_path = os.path.join(self.tests_path, self.fixtures_dir)

    def format(self, content, extra={}):
        """
        Format given string to include some values related to this application.

        Arguments:
            content (str): Content string to format with possible values.

        Returns:
            str: Given string formatted with possible values.
        """
        variables = {
            "HOMEDIR": os.path.expanduser("~"),
            "PACKAGE": self.package_path,
            "APPLICATION": self.application_path,
            "TESTS": self.tests_path,
            "FIXTURES": self.fixtures_path,
            "SANDBOX": self.sandbox_path,
            "STATICS": self.statics_path,
            "VERSION": vv.__version__,
        }
        if extra:
            variables.update(extra)

        return content.format(**variables)


@pytest.fixture(scope="function")
def temp_builds_dir(tmpdir):
    """
    Prepare a temporary build directory
    """
    fn = tmpdir.mkdir("sandbox-tests")
    return fn


@pytest.fixture(scope="module")
def tests_settings():
    """
    Initialize and return settings for tests.

    Example:
        You may use it in tests like this: ::

            def test_foo(tests_settings):
                print(tests_settings.package_path)
                print(tests_settings.format("foo: {VERSION}"))
    """
    return ApplicationTestSettings()
