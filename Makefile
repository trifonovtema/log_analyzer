.PHONY: install lint format test run pre-commit

install:
	poetry install

lint:
	poetry run black app
	poetry run isort app

format:
	make lint

test:
	PYTHONPATH="$(PWD)" poetry run python -m pytest --import-mode=importlib

run:
	poetry run python -m log_analyzer.main --config ./sample_config.json

pre-commit:
	poetry run pre-commit run --all-files
