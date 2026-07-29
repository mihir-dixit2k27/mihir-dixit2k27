.PHONY: help update lint fmt

# Default target
help:
	@echo ""
	@echo "  mihir-dixit2k27 profile README — available targets"
	@echo ""
	@echo "  make update        Run all README update scripts"
	@echo "  make update-blog   Update blog posts only"
	@echo "  make update-act    Update activity / OSS metrics only"
	@echo "  make lint          Lint Python scripts with ruff"
	@echo "  make fmt           Auto-format Python scripts with ruff"
	@echo ""

# Run all update scripts in order (same as the weekly GitHub Actions workflow)
update:
	python scripts/update_readme.py

# Run blog updater only
update-blog:
	python scripts/update_blog.py

# Run activity/metrics updater only
update-act:
	python scripts/update_activity.py

# Lint
lint:
	ruff check scripts/

# Format
fmt:
	ruff format scripts/
