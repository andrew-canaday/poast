.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

# Hack to get the directory this makefile is in:
MKFILE_PATH := $(lastword $(MAKEFILE_LIST))
MKFILE_DIR := $(notdir $(patsubst %/,%,$(dir $(MKFILE_PATH))))
MKFILE_ABSDIR := $(abspath $(MKFILE_DIR))

# Detect runtime:
ifdef TRAVIS
IS_RUNTIME_TRAVIS := true
else
IS_RUNTIME_TRAVIS := false
endif # TRAVIS

IS_RUNTIME_DOCKER := $(shell \
	if [ -f '/.dockerenv' -o -f '/proc/self/cgroup/docker' ]; then \
		echo "true"; \
	else \
		echo "false"; \
	fi )

#-------------------------------------------------------------------------------
# REQUIRE A VENV:
#
# In order to check for the venv on every invocation of make, we include a file
# that doesn't exist, with a target declared as PHONY (above), and then have
# the target used to create it check for the VIRTUAL_ENV env var. If undefined
# use the in-built $(error ...) function to exit make with a descriptive error.
-include ensure_venv
ensure_venv: # Ensure a virtual environment is active
ifndef VIRTUAL_ENV
ifeq ($(IS_RUNTIME_TRAVIS),true)
	# Virtual env not required for travis builds:
	@echo "Drone build detected ($(TRAVIS))"
else
ifeq ($(IS_RUNTIME_DOCKER),true)
	@echo "Docker build detected"
else
	$(error 'No virtual env detected! See README.md for init instructions')
endif # DOCKER
endif # TRAVIS
endif # VIRTUAL_ENV
#-------------------------------------------------------------------------------
help_spacing := 14
help: ## Print this makefile help menu
	@echo 'Targets:'
	@grep '^[a-z_\-]\{1,\}:.*##' $(MAKEFILE_LIST) \
		| sed 's/^\([a-z_\-]\{1,\}\): *\(.*[^ ]\) *## *\(.*\)/\1:\t\3 (\2)/g' \
		| sed 's/^\([a-z_\-]\{1,\}\): *## *\(.*\)/\1:\t\2/g' \
		| awk '{$$1 = sprintf("%-$(help_spacing)s", $$1)} 1' \
		| sed 's/^/  /'

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -rf {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean-test: ## remove test and coverage artifacts
	rm -rf .tox/
	rm -f .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache

lint: ## check style with flake8
	flake8 poast tests

test: ## run tests quickly with the default Python
	pytest

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source poast -m pytest
	coverage report -m
	coverage html

docs: ## generate Sphinx HTML documentation, including API docs
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

man: docs ## generate Sphinx manpage documentation, including API docs
	$(MAKE) -C docs man

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.md' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
