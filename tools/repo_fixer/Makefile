# Repo Fixer Tool
# Fix and standardize repository configurations

.PHONY: help install test fix check setup-config

PYTHON := python3
SCRIPT := repo_fixer.py
CONFIG := config.yaml

help:
	@echo "🔧 Repo Fixer Tool"
	@echo ""
	@echo "Setup:"
	@echo "  make install        - Install dependencies"
	@echo "  make test           - Test tool functionality"
	@echo ""
	@echo "Repository Fixing:"
	@echo "  make fix REPO=/path/to/repo - Fix repository configuration"
	@echo "  make check REPO=/path/to/repo - Check repository without fixing"
	@echo "  make fix-current    - Fix current directory repository"
	@echo "  make check-current  - Check current directory repository"
	@echo ""
	@echo "Batch Operations:"
	@echo "  make fix-all        - Fix all repositories in workspace"
	@echo "  make dry-run        - Show what would be fixed without making changes"
	@echo ""  
	@echo "Configuration:"
	@echo "  make show-config    - Show current configuration"
	@echo "  make edit-config    - Edit configuration file"
	@echo ""
	@echo "Templates:"
	@echo "  make show-templates - Show available templates"
	@echo "  make test-templates - Test template generation"
	@echo ""
	@echo "Examples:"
	@echo "  make fix REPO=~/projects/my-repo"
	@echo "  make check-current"
	@echo "  make dry-run"

install:
	@echo "📦 Repo Fixer dependencies managed by uv"
	@echo "✅ No separate installation needed - use 'uv run' commands"

test:
	@echo "🧪 Testing Repo Fixer..."
	@uv run python $(SCRIPT) --help > /dev/null 2>&1 && echo "✅ Script working!" || echo "⚠️  Check if script supports --help"
	@echo "🧪 Testing configuration..."
	@[ -f $(CONFIG) ] && echo "✅ Config file exists" || echo "⚠️  Config file missing"

# Main fixing commands
fix:
	@if [ -z "$(REPO)" ]; then \
		echo "❌ Error: REPO parameter required"; \
		echo "   Usage: make fix REPO=/path/to/repository"; \
		exit 1; \
	fi
	@echo "🔧 Fixing repository: $(REPO)"
	@uv run python $(SCRIPT) --repo $(REPO) --fix

check:
	@if [ -z "$(REPO)" ]; then \
		echo "❌ Error: REPO parameter required"; \
		echo "   Usage: make check REPO=/path/to/repository"; \
		exit 1; \
	fi
	@echo "🔍 Checking repository: $(REPO)"
	@uv run python $(SCRIPT) --repo $(REPO) --check

fix-current:
	@echo "🔧 Fixing current directory repository..."
	@uv run python $(SCRIPT) --repo . --fix

check-current:
	@echo "🔍 Checking current directory repository..."
	@uv run python $(SCRIPT) --repo . --check

# Batch operations
fix-all:
	@echo "🔧 Fixing all repositories in workspace..."
	@uv run python $(SCRIPT) --fix-all

dry-run:
	@echo "🔍 Dry run - showing what would be fixed..."
	@uv run python $(SCRIPT) --dry-run

# Configuration
show-config:
	@echo "🔧 Repo Fixer Configuration:"
	@if [ -f $(CONFIG) ]; then \
		echo "✅ Config file: $(CONFIG)"; \
		cat $(CONFIG); \
	else \
		echo "❌ Config file not found: $(CONFIG)"; \
	fi

edit-config:
	@echo "📝 Opening configuration file..."
	@$${EDITOR:-nano} $(CONFIG)

# Templates
show-templates:
	@echo "📋 Available Templates:"
	@echo ""
	@echo "Poetry template:"
	@[ -f poetry_template.txt ] && cat poetry_template.txt || echo "❌ poetry_template.txt not found"
	@echo ""
	@echo "Tests workflow template:" 
	@[ -f tests_workflow_template.txt ] && cat tests_workflow_template.txt || echo "❌ tests_workflow_template.txt not found"

test-templates:
	@echo "🧪 Testing template generation..."
	@echo "✅ Poetry template: $$([ -f poetry_template.txt ] && echo 'Present' || echo 'Missing')"
	@echo "✅ Tests workflow template: $$([ -f tests_workflow_template.txt ] && echo 'Present' || echo 'Missing')"

# Development and testing
dev-test:
	@echo "🧪 Running development tests..."
	@if [ -d tests/ ]; then \
		echo "Running pytest tests..."; \
		uv run python -m pytest tests/ -v; \
	else \
		echo "⚠️  No tests directory found"; \
	fi

run-tests:
	@echo "🧪 Running unit tests..."
	@uv run python -m pytest tests/ -v

test-precommit:
	@echo "🧪 Testing pre-commit functionality..."
	@uv run python -m pytest tests/test_precommit.py -v

test-project-name:
	@echo "🧪 Testing project name functionality..."
	@uv run python -m pytest tests/test_project_name.py -v

# Quick fixes for common issues
fix-poetry:
	@echo "🔧 Fixing Poetry configuration in current repo..."
	@uv run python $(SCRIPT) --repo . --fix-poetry

fix-github-actions:
	@echo "🔧 Fixing GitHub Actions in current repo..."
	@uv run python $(SCRIPT) --repo . --fix-actions

fix-precommit:
	@echo "🔧 Fixing pre-commit configuration in current repo..."
	@uv run python $(SCRIPT) --repo . --fix-precommit

# Statistics
stats:
	@echo "📊 Repo Fixer Statistics:"
	@echo "Config file: $$([ -f $(CONFIG) ] && echo '✅ Present' || echo '❌ Missing')"
	@echo "Templates: $$(ls -1 *_template.txt 2>/dev/null | wc -l || echo 0)"
	@echo "Tests: $$([ -d tests/ ] && ls -1 tests/test_*.py 2>/dev/null | wc -l || echo 0)"

# Clean up
clean:
	@echo "🧹 Cleaning up temporary files..."
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete
	@echo "✅ Cleanup complete!"