RUN := uv run python -B
PYPROJECT_TOML := pyproject.toml

ARGS ?= config
FLAKE8 := $(RUN) -m flake8
MYPY := $(RUN) -m mypy

INSTALL_STAMP := .installed

$(INSTALL_STAMP): $(PYPROJECT_TOML)
	uv sync
	@touch $(INSTALL_STAMP)

all: run

install: $(INSTALL_STAMP)

run: $(INSTALL_STAMP)
	@$(RUN) pac-man.py $(ARGS)

debug: $(INSTALL_STAMP)
	@$(RUN) pac-man.py $(ARGS)

lint: $(INSTALL_STAMP)
	$(FLAKE8) src
	$(MYPY) src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	@rm -rf $(INSTALL_STAMP)
	@rm -rf .mypy_cache .venv
	@find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

fclean: clean
	@rm -rf .venv

.PHONY: all install run debug lint clean fclean
