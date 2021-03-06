default: normal lint test

normal:
	isort .

lint:
	flake8 .

test:
	coverage erase
	coverage run --source=django_amp_renderer -m pytest
	coverage report -m

dev:
	pip install -r requirements/dev.txt
