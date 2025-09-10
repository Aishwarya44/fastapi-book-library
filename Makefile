VENV_DIR := venv
PYTHON := python3
PIP := $(VENV_DIR)/bin/pip
ACTIVATE := source $(VENV_DIR)/bin/activate

all:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment"; \
		$(PYTHON) -m venv $(VENV_DIR); \
	fi
	@echo "Installing dependencies"
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "All requirements are installed"
	@echo "Activating virtual environment $(ACTIVATE)"