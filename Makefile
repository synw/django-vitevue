VENV_PATH=.venv
PYTHON_INTERPRETER=python3
PIP=$(VENV_PATH)/bin/pip
TWINE=$(VENV_PATH)/bin/twine
DJANGO_MANAGE=$(VENV_PATH)/bin/python sandbox/manage.py
FLAKE=$(VENV_PATH)/bin/flake8
PYTEST=$(VENV_PATH)/bin/pytest

DEMO_DJANGO_SECRET_KEY=samplesecretfordev
PACKAGE_NAME=django-vitevue
PACKAGE_SLUG=`echo $(PACKAGE_NAME) | tr '-' '_'`
APPLICATION_NAME=vv

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  install             -- to install this project with virtualenv and Pip"
	@echo "  clean               -- to clean EVERYTHING (Warning)"
	@echo "  clean-var           -- to clean data (uploaded medias, database, etc..)"
	@echo "  clean-install       -- to clean Python side installation"
	@echo "  clean-pycache       -- to remove all __pycache__, this is recursive from current directory"
	@echo
	@echo "  run                 -- to run Django development server"
	@echo "  migrate             -- to apply demo database migrations"
	@echo "  migrations          -- to create new migrations for application after changes"
	@echo
	@echo "  flake               -- to launch Flake8 checking"
	@echo "  test                -- to launch base test suite using Pytest"
	@echo "  test-initial        -- to launch tests with pytest and re-initialized database (for after new application or model changes)"
	@echo "  quality             -- to launch Flake8 checking and every tests suites"
	@echo
	@echo "  check-release       -- to check package release before uploading it to PyPi"
	@echo "  publish             -- to release package for latest version on PyPi (once release has been pushed to repository)"
	@echo

clean-pycache:
	@echo ""
	@echo "==== Clear Python cache ===="
	@echo ""
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache

clean-install:
	@echo ""
	@echo "==== Clear installation ===="
	@echo ""
	rm -Rf $(VENV_PATH)
	rm -Rf $(PACKAGE_SLUG).egg-info
.PHONY: clean-install

clean-var:
	@echo ""
	@echo "==== Clear var/ directory ===="
	@echo ""
	rm -Rf var
.PHONY: clean-var

clean: clean-var clean-doc clean-install clean-pycache
.PHONY: clean

venv:
	@echo ""
	@echo "==== Install virtual environment ===="
	@echo ""
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
	# This is required for those ones using old distribution
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools
.PHONY: venv

create-var-dirs:
	@mkdir -p var/db
	@mkdir -p var/static/css
	@mkdir -p var/media
	@mkdir -p sandbox/media
	@mkdir -p sandbox/static/css
.PHONY: create-var-dirs

install: venv create-var-dirs
	@echo ""
	@echo "==== Install everything for development ===="
	@echo ""
	$(PIP) install -e .[dev]
	${MAKE} migrate
.PHONY: install

migrations:
	@echo ""
	@echo "==== Making application migrations ===="
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE) makemigrations $(APPLICATION_NAME)
.PHONY: migrations

migrate:
	@echo ""
	@echo "==== Apply pending migrations ===="
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE) migrate
.PHONY: migrate

run:
	@echo ""
	@echo "==== Running development server ===="
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE) runserver 0.0.0.0:8001
.PHONY: run

flake:
	@echo ""
	@echo "==== Flake ===="
	@echo ""
	$(FLAKE) --show-source $(APPLICATION_NAME)
	$(FLAKE) --show-source tests
.PHONY: flake

test:
	@echo ""
	@echo "==== Tests ===="
	@echo ""
	$(PYTEST) -vv --reuse-db tests/
	rm -Rf var/media-tests/
.PHONY: test

test-initial:
	@echo ""
	@echo "==== Tests from zero ===="
	@echo ""
	$(PYTEST) -vv --reuse-db --create-db tests/
	rm -Rf var/media-tests/
.PHONY: test-initial

build:
	@echo ""
	@echo "==== Build package ===="
	@echo ""
	rm -rf build *.egg-info
	rm -Rf dist
	$(VENV_PATH)/bin/python setup.py sdist
.PHONY: build

publish:
	@echo ""
	@echo "==== Release ===="
	@echo ""
	$(TWINE) upload dist/*
.PHONY: publish

check-release:
	@echo ""
	@echo "==== Check package ===="
	@echo ""
	$(TWINE) check dist/*
.PHONY: check-release

pycheck:
	@echo ""
	@echo "==== Running pycheck on package ===="
	@echo ""
	pycheck
.PHONY: pycheck

quality: test-initial check-release pycheck
.PHONY: quality
