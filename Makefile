VENV_DIR := .venv
UV := $(shell command -v uv 2>/dev/null || echo $(HOME)/.local/bin/uv)

default: sync configure format lint check test

sync-spec:
	@echo "Syncing configuration with global spec..."
	@nitpick fix > /dev/null || true
	@echo "...done."

configure-spec:
	@echo "Checking configuration against global spec..."
	@nitpick check
	@printf "\e[1mConfiguration is in sync!\e[0m\n\n"

sync: sync-spec
	@printf "\e[1mSync complete!\e[0m\n\n"

configure: configure-spec

format:
	@echo "Formatting Python docstrings..."
	@docformatter . -r --in-place --wrap-descriptions=79 --exclude dist prof build .git .venv
	@echo "...done."

	@echo
	@echo "Formatting Python files..."
	@echo "  1. Ruff Format"
	@ruff format . > /dev/null
	@echo "  2. Ruff Check (fix only)"
	@ruff check --fix-only . --quiet
	@echo "  3. Add trailing commas"
	@find . \( -path ./lib -o -path ./bin -o -path ./dist -o -path ./prof -o -path ./build -o -path ./.git -o -path ./.venv \) -prune -o -name '*.py' -print0 | xargs -0 -I{} sh -c 'add-trailing-comma "{}" || true'
	@echo "  4. Ruff Format (again)"
	@ruff format . --quiet
	@echo "  5. Ruff Check (fix only, again)"
	@ruff check --fix-only . --quiet
	@echo "...done."
	@echo

lint:
	@echo "Checking for Python formatting issues which can be fixed automatically..."
	@echo "  1. Ruff Format (check only)"
	@ruff format . --diff > /dev/null 2>&1 || (printf 'Found files which need to be auto-formatted. Run \e[1mmake format\e[0m and re-lint.\n'; exit 1)
	@echo "...done. No issues found."

	@echo
	@echo "Running Python linter..."
	@echo "  1. Ruff Check"
	@ruff check . --quiet
	@echo "  2. Flake8"
	@flake8 .
	@echo "...done. No issues found."
	@echo

check-py:
	@echo "Running Python type checks..."
	@ty check .
	@echo "...done. No issues found."

check: check-py

test:
	find . -name "*.pyc" -delete
	coverage erase
	coverage run --source=django_amp_renderer -m pytest --ignore=bin --ignore=lib --ignore=dist --ignore=prof --ignore=build
	coverage report -m --fail-under 90

setup:
	@if [ ! -x "$(UV)" ]; then curl -LsSf https://astral.sh/uv/install.sh | sh; fi
	$(UV) venv --prompt "django-amp-renderer" $(VENV_DIR)
	$(UV) pip install --python $(VENV_DIR) -r requirements/test.txt
	@printf "\n\e[1mSetup complete!\e[0m\n\n"
	@echo "Activate the virtual environment with:"
	@echo
	@echo "	source $(VENV_DIR)/bin/activate"
	@echo

install:
	$(UV) pip install -r requirements/test.txt

.PHONY: default sync sync-spec configure configure-spec format lint check check-py test setup install
