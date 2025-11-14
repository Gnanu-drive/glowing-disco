# Makefile for Data Version Control Project
# Compatible with Windows, macOS, and Linux

# Detect OS
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
    PYTHON := python
    RM := del /Q
    RM_RF := rmdir /S /Q
    VENV_BIN := venv\Scripts
    VENV_ACTIVATE := $(VENV_BIN)\activate
    MKDIR := if not exist
else
    DETECTED_OS := $(shell uname -s)
    PYTHON := python3
    RM := rm -f
    RM_RF := rm -rf
    VENV_BIN := venv/bin
    VENV_ACTIVATE := . $(VENV_BIN)/activate
    MKDIR := mkdir -p
endif

.PHONY: help setup install init-dvc download-data run clean test info

help:
	@echo "Data Version Control Project - Makefile"
	@echo "========================================"
	@echo "Detected OS: $(DETECTED_OS)"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Create virtual environment"
	@echo "  make install      - Install dependencies from requirements.txt"
	@echo "  make init-dvc     - Initialize DVC"
	@echo "  make download-data - Download and prepare sample data"
	@echo "  make run          - Run the complete workflow"
	@echo "  make clean        - Remove generated files and virtual environment"
	@echo "  make test         - Test the environment"
	@echo "  make info         - Display system information"

info:
	@echo "System Information:"
	@echo "OS: $(DETECTED_OS)"
	@echo "Python: $(PYTHON)"
	@$(PYTHON) --version

setup:
	@echo "Creating virtual environment for $(DETECTED_OS)..."
	$(PYTHON) -m venv venv
	@echo "Virtual environment created successfully!"
	@echo "To activate:"
ifeq ($(DETECTED_OS),Windows)
	@echo "  venv\Scripts\activate"
else
	@echo "  source venv/bin/activate"
endif

install: setup
	@echo "Installing dependencies for $(DETECTED_OS)..."
ifeq ($(DETECTED_OS),Windows)
	$(VENV_BIN)\pip install --upgrade pip
	$(VENV_BIN)\pip install -r requirements.txt
else
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements.txt
endif
	@echo "Dependencies installed successfully!"

init-dvc:
	@echo "Initializing DVC..."
ifeq ($(DETECTED_OS),Windows)
	$(VENV_BIN)\dvc init
else
	$(VENV_BIN)/dvc init
endif
	@echo "DVC initialized successfully!"

download-data:
	@echo "Downloading and preparing sample data..."
ifeq ($(DETECTED_OS),Windows)
	$(VENV_BIN)\python data_pipeline.py --download
else
	$(VENV_BIN)/python data_pipeline.py --download
endif
	@echo "Data downloaded successfully!"

run:
	@echo "Running complete DVC workflow..."
ifeq ($(DETECTED_OS),Windows)
	$(VENV_BIN)\python data_pipeline.py --all
else
	$(VENV_BIN)/python data_pipeline.py --all
endif
	@echo "Workflow completed successfully!"

test:
	@echo "Testing environment..."
ifeq ($(DETECTED_OS),Windows)
	$(VENV_BIN)\python -c "import pandas; import numpy; import sklearn; import dvc; print('All dependencies are working!')"
else
	$(VENV_BIN)/python -c "import pandas; import numpy; import sklearn; import dvc; print('All dependencies are working!')"
endif

clean:
	@echo "Cleaning up..."
ifeq ($(DETECTED_OS),Windows)
	-$(RM_RF) venv
	-$(RM_RF) data
	-$(RM_RF) outputs
	-$(RM_RF) __pycache__
	-$(RM) *.pyc
else
	-$(RM_RF) venv
	-$(RM_RF) data
	-$(RM_RF) outputs
	-$(RM_RF) __pycache__
	-$(RM) *.pyc
endif
	@echo "Cleanup completed!"
