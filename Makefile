CURRENT_SIGN_SETTING := $(shell git config commit.gpgSign)

.PHONY: clean-pyc clean-build docs

help:
	@echo "clean - run all cleanup tasks"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "release - package and upload a release"
	@echo "dist - package"

clean: clean-build clean-pyc

clean-build:
	python setup.py clean
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs *.egg-info
	find . -name __pycache__ -exec rm -rf {} +
	rm -rf .coverage* htmlcov
	rm -rf build docs/_build docs/build

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 cwf2neo

lint-roll:
	isort --recursive cwf2neo
	$(MAKE) lint

devbuild: venv
	venv/bin/python setup.py install
	venv/bin/pip install -r requirements.txt

test: devbuild
	venv/bin/pytest cwf2neo/tests

build-docs:
	sphinx-build -T -D language=en docs/ docs/_build/html
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

docs: build-docs
	open docs/_build/html/index.html

release: clean
	git config commit.gpgSign true
	bumpversion minor
	git push upstream && git push upstream --tags
	python setup.py sdist bdist_wheel
	twine upload dist/*
	git config commit.gpgSign "$(CURRENT_SIGN_SETTING)"

dist: clean
	python setup.py sdist bdist_wheel
	ls -l dist

install: clean
	python setup.py install

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate
