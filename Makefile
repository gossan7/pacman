UV := uv run
RUN := $(UV) python -B
PYPROJECT_TOML := pyproject.toml

ARGS ?= config.json
FLAKE8 := $(RUN) -m flake8
MYPY := $(RUN) -m mypy

DIST_DIR := build/dist
WORK_DIR := build/work
SPEC_DIR := build/spec

INSTALL_STAMP := .installed

$(INSTALL_STAMP): $(PYPROJECT_TOML)
	uv sync
	@touch $(INSTALL_STAMP)

all: run

install: $(INSTALL_STAMP)

run: $(INSTALL_STAMP)
	@$(RUN) pac-man.py $(ARGS)

package: $(INSTALL_STAMP)
	$(UV) pyinstaller --onedir --name pac-man \
	--add-data "$(CURDIR)/assets:assets" \
	--add-data "$(CURDIR)/config.json:." \
	--distpath $(DIST_DIR) \
	--workpath $(WORK_DIR) \
	--specpath $(SPEC_DIR) \
	$(CURDIR)/pac-man.py --noconfirm

debug: $(INSTALL_STAMP)
	@$(RUN) -m pdb pac-man.py $(ARGS)

lint: $(INSTALL_STAMP)
	$(FLAKE8) src pac-man.py
	$(MYPY) src pac-man.py --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	@rm -rf $(INSTALL_STAMP)
	@rm -rf .mypy_cache
	@find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

fclean: clean
	@rm -rf .venv build

.PHONY: all install run package debug lint clean fclean
