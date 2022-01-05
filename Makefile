SHELL:=/bin/bash

PROJECT := heroku_guardian

# ---------------------------------------------------------------------------------------------------------------------
# Environment setup and management
# ---------------------------------------------------------------------------------------------------------------------
setup-env:
	python3 -m venv ./venv && source venv/bin/activate
	python3 -m pip install -r requirements.txt
setup-dev: setup-env
	python3 -m pip install -r requirements-dev.txt
# ---------------------------------------------------------------------------------------------------------------------
# Documentation for ReadThedocs
# Leave doc commands for reference
# ---------------------------------------------------------------------------------------------------------------------
build-docs: setup-dev
	mkdocs build
serve-docs: setup-dev
	mkdocs serve --dev-addr "127.0.0.1:8001"
# ---------------------------------------------------------------------------------------------------------------------
# Package building and publishing
# ---------------------------------------------------------------------------------------------------------------------
build: setup-env clean
	python3 -m pip install --upgrade setuptools wheel
	python3 -m setup -q sdist bdist_wheel
install: build
	python3 -m pip install -q ./dist/heroku-guardian*.tar.gz
	heroku-guardian --help
uninstall:
	python3 -m pip uninstall heroku-guardian -y
	python3 -m pip uninstall -r requirements.txt -y
	python3 -m pip uninstall -r requirements-dev.txt -y
	python3 -m pip freeze | xargs python3 -m pip uninstall -y
publish: build
	python3 -m pip install --upgrade twine
	python3 -m twine upload dist/*
	python3 -m pip install heroku-guardian
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*.egg-link' -delete
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
# ---------------------------------------------------------------------------------------------------------------------
# Python Testing
# ---------------------------------------------------------------------------------------------------------------------
test: setup-dev
	python3 -m coverage run -m pytest -v
security-test: setup-dev
	bandit -r ./${PROJECT}/
# ---------------------------------------------------------------------------------------------------------------------
# Linting and formatting
# ---------------------------------------------------------------------------------------------------------------------
fmt: setup-dev
	black ${PROJECT}/
lint: setup-dev
	pylint ${PROJECT}/
# ---------------------------------------------------------------------------------------------------------------------
# Miscellaneous Development
# ---------------------------------------------------------------------------------------------------------------------
count-loc:
	echo "If you don't have tokei installed, you can install it with 'brew install tokei'"
	echo "Website: https://github.com/XAMPPRocky/tokei#installation'"
	tokei ./* --exclude --exclude '**/*.html' --exclude '**/*.json'