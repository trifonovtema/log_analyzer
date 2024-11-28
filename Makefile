.PHONY: install lint format test run pre-commit

install:
	poetry install

lint:
	poetry run black log_analyzer
	poetry run isort log_analyzer

format:
	make lint

test:
	poetry run pytest

run:
	poetry run python -m log_analyzer.main --config ./sample_config.json

pre-commit:
	poetry run pre-commit run --all-files
