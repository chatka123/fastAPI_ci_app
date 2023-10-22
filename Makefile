CODE_FOLDERS := src
TEST_FOLDERS := tests

.PHONY: update test lint security_checks

install:
	poetry install

update:
	poetry lock

test:
	poetry run pytest

format:
	black .

lint:
	black --check .
	isort $(CODE_FOLDERS) $(TEST_FOLDERS)
	flake8 $(CODE_FOLDERS) $(TEST_FOLDERS)
	pylint $(CODE_FOLDERS) $(TEST_FOLDERS)
	mypy $(CODE_FOLDERS) $(TEST_FOLDERS)
