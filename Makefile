.SILENT:

SHELL := /bin/bash

VERSION := $(shell ./setup.py --version)

all: build

build:
	./setup.py build

bdist:
	./setup.py bdist

sdist:
	./setup.py sdist

install:
	./setup.py install

test:
	echo 'Python 2:'
	python2 ./setup.py test
	echo
	echo 'Python 3:'
	python3 ./setup.py test

clean:
	./setup.py clean > /dev/null 2>&1 || true
	rm -rf ./build/ ./dist/ ./*.egg-info/
	find . -type d -name '__pycache__' -exec rm -rf '{}' ';' -prune
	find . -type f -name '*.pyc' -delete

release: clean
	# Check for clean working directory
	[[ -z "$$( git status --porcelain 2>&1 )" ]] || echo 'Unclean working directory:'
	[[ -z "$$( git status --porcelain 2>&1 )" ]] || git status --porcelain
	[[ -z "$$( git status --porcelain 2>&1 )" ]] || true
	# Check for existing tag for this version
	if git tag --list | grep -xF --color=never 'v$(VERSION)'; then echo 'Tag already exists:'; else true; fi
	if git tag --list | grep -xF --color=never 'v$(VERSION)'; then false; else true; fi
	# Create tag
	git tag -a 'v$(VERSION)' -m 'version $(VERSION)'
	git push --tags
	# Upload to PyPI
	./setup.py register -r pypi
	./setup.py sdist upload -r pypi

.PHONY: all build bdist sdist install test release clean

