PROJECT_NAME = ProbablyOverthinkingBlog
PYTHON_VERSION = 3.11
PYTHON_INTERPRETER = python

.PHONY: create_environment delete_environment install clean test help

# Default target
help:
	@echo "Available targets:"
	@echo "  create_environment  - Create conda environment with mamba"
	@echo "  delete_environment  - Remove conda environment"
	@echo "  install             - Update environment from environment.yml"
	@echo "  clean               - Remove temporary files and caches"
	@echo "  test                - Run tests (if available)"
	@echo "  help                - Show this help message"

# Create conda environment using mamba
create_environment:
	mamba env create -f environment.yml
	@echo ">>> mamba env created. Activate with:\nconda activate $(PROJECT_NAME)"

# Delete conda environment
delete_environment:
	mamba env remove --name $(PROJECT_NAME)

# Update environment from environment.yml
install:
	mamba env update -f environment.yml --name $(PROJECT_NAME)

# Clean temporary files
clean:
	-find . -type f -name '*.pyc' -delete
	-find . -type d -name '__pycache__' -delete
	-find . -type d -name '.pytest_cache' -delete
	-find . -type d -name '.ipynb_checkpoints' -delete
	-rm -rf .ruff_cache/
	-rm -rf build/
	-rm -rf dist/
	-rm -rf *.egg-info

# Run tests
test:
	@echo "No tests configured yet"
