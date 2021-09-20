from os import path
from setuptools import setup, find_packages


version = __import__("vv").__version__

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="django-vitevue",
    packages=find_packages(),
    include_package_data=True,
    version=version,
    description="Manage Vitejs frontends for Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="synw",
    author_email="synwe@yahoo.com",
    url="https://github.com/synw/django-vitevue",
    download_url="https://github.com/synw/django-vitevue/releases/tag/" + version,
    keywords=["django", "vitejs"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        "django-introspection",
    ],
    zip_safe=False,
)
