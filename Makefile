# Required executables
ifeq (, $(shell which python))
 $(error "No python on PATH.")
endif
PIPENV_COM := python -m pipenv
ifeq (, $(shell $(PIPENV_COM)))
 $(error "Pipenv not available in Python installation.")
endif

# Suppress warning if pipenv is started inside .venv
export PIPENV_VERBOSITY = 1
# Use relative .venv folder instead of home-folder based
export PIPENV_VENV_IN_PROJECT = 1
# Ignore existing venvs
export PIPENV_IGNORE_VIRTUALENVS = 1
# Make sure we are running with an explicit encoding
export LC_ALL = C
export LANG = C.UTF-8
# Set configuration folder to venv
export PYPE_CONFIG_FOLDER = $(shell pwd)/.venv/.pype-cli
# Process variables
VERSION = $(shell python setup.py --version)
PY_FILES := setup.py akai_mpkmini_mkii_ctrl tests
LAST_VERSION := $(shell git tag | sort --version-sort -r | head -n1)
VERSION_HASH := $(shell git show-ref -s $(LAST_VERSION))

all: clean venv build

venv: clean
	@echo Initialize virtualenv, i.e., install required packages etc.
	$(PIPENV_COM) install --dev

shell:
	@echo Initialize virtualenv and open a new shell using it
	pipenv shell

clean:
	@echo Clean project base
	find . -type d \
	-name ".venv" -o \
	-name ".tox" -o \
	-name ".ropeproject" -o \
	-name ".mypy_cache" -o \
	-name ".pytest_cache" -o \
	-name "__pycache__" -o \
	-iname "*.egg-info" -o \
	-name "build" -o \
	-name "dist" \
	|xargs rm -rfv

	find . -type f \
	-name "pyproject.toml" -o \
	-name "Pipfile.lock" \
	|xargs rm -rfv


test:
	@echo Run all tests in default virtualenv
	pipenv run py.test tests

testall:
	@echo Run all tests against all virtualenvs defined in tox.ini
	pipenv run tox -c setup.cfg tests

isort:
	@echo Check for incorrectly sorted imports
	pipenv run isort --check-only $(PY_FILES)

isort-apply:
	@echo Check for incorrectly sorted imports
	pipenv run isort $(PY_FILES)

mypy:
	@echo Run static code checks against source code base
	pipenv run mypy akai_mpkmini_mkii_ctrl
	pipenv run mypy tests

lint:
	@echo Run code formatting checks against source code base
	pipenv run flake8 akai_mpkmini_mkii_ctrl tests

build: test mypy isort lint
	@echo Run setup.py-based build process to package application
	pipenv run python setup.py bdist_wheel

install: all
	@echo Install application
	pip install --upgrade --user dist/*.whl

run:
	@echo Execute akai_mpkmini_mkii_ctrl directly
	pipenv run python -m akai_mpkmini_mkii_ctrl

publish: all
	@echo Publish pype to pypi.org
	pipenv run twine upload dist/*

release:
	@echo Commit release - requires NEXT_VERSION to be set
	test $(NEXT_VERSION)
	sed -i '' "s/version='[0-9\.]*',/version='$(NEXT_VERSION)',/" setup.py
	git commit -am "Release $(NEXT_VERSION)"
	git tag $(NEXT_VERSION)
	git push origin $(NEXT_VERSION)
	git push

changelog:
	@echo Return changelog since last version tag
	git --no-pager log --pretty=format:"- %s" $(VERSION_HASH)..HEAD |cat
