# Install dependencies
.PHONY: install
install:
	pip install -r requirements.txt
	pre-commit install

# Run lint
.PHONY: lint
lint:
	pre-commit run --all-files

# Run tests
.PHONY: test
test: 
	pytest -v -rs --show-capture=no

.PHONY: lint-and-test
lint-and-test: lint test ;