# Variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python

# Install dependencies
.PHONY: install
install:
	pip install -r requirements.txt
	pre-commit install

# Run lint
.PHONY: lint
lint:
	mypy server
	flake8 server

# Run tests
.PHONY: test
test:
	cd server && python -m pytest -v -rs --show-capture=no

.PHONY: lint-and-test
lint-and-test: lint test ;