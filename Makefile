.PHONY: install lint format test run pre-commit

install:
	poetry install

lint:
	poetry run black app
	poetry run isort app
	poetry run mypy app

format:
	make lint

test:
	poetry run python -m pytest

run:
	poetry run python -m app.main --config ./sample_config.json

pre-commit:
	poetry run pre-commit run --all-files
