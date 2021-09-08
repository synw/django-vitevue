from setuptools import setup, find_packages


version = __import__("vv").__version__

setup(
    name="django-vitevue",
    packages=find_packages(),
    include_package_data=True,
    version=version,
    description="Vite and Vuejs Django tools",
    author="synw",
    author_email="synwe@yahoo.com",
    url="https://github.com/synw/django-vitevue",
    download_url="https://github.com/synw/django-vitevue/releases/tag/" + version,
    keywords=["django", "vuejs"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django :: 1.11",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        "django-introspection",
    ],
    zip_safe=False,
)
