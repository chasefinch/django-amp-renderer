default: format lint test

format:
	isort .

lint:
	flake8 .

test:
	coverage erase
	coverage run --source=django_amp_renderer -m pytest
	coverage report -m

develop:
	pip install -r requirements/develop.txt
