.PHONY: install clean test help

# Default target
help:
	@echo "Available targets:"
	@echo "  install    - Install Python dependencies"
	@echo "  clean      - Remove temporary files and caches"
	@echo "  test       - Run tests (if available)"
	@echo "  help       - Show this help message"

# Install dependencies
install:
	pip install -r requirements.txt

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
