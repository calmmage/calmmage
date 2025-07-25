# Project Discoverer Tool
# Find and discover projects across the workspace

.PHONY: help install test find update-index

PYTHON := python3
CLI := pd_cli.py

help:
	@echo "🔍 Project Discoverer Tool"
	@echo ""
	@echo "Setup:"
	@echo "  make install        - Install dependencies"
	@echo "  make test           - Test tool functionality"
	@echo "  make setup-config   - Setup configuration file"
	@echo ""
	@echo "Project Discovery:"
	@echo "  make find QUERY=search_term - Find projects by name/keyword"
	@echo "  make update-index   - Update project discovery index"
	@echo ""
	@echo "Configuration:"
	@echo "  make show-config    - Show current configuration"
	@echo "  make edit-config    - Open configuration for editing"
	@echo ""
	@echo "Examples:"
	@echo "  make find QUERY=botspot"
	@echo "  make find QUERY=telegram"
	@echo "  make find QUERY=scheduler"

install:
	@echo "📦 Project Discoverer dependencies managed by uv"
	@echo "✅ No separate installation needed - use 'uv run' commands"

test:
	@echo "🧪 Testing Project Discoverer..."
	@uv run typer $(CLI) run --help > /dev/null && echo "✅ CLI working!" || echo "❌ CLI failed!"

# Main discovery command
find:
	@if [ -z "$(QUERY)" ]; then \
		echo "❌ Error: QUERY parameter required"; \
		echo "   Usage: make find QUERY=search_term"; \
		exit 1; \
	fi
	@echo "🔍 Searching for projects matching: $(QUERY)"
	@uv run typer $(CLI) run find $(QUERY)

# Index management (if supported)
update-index:
	@echo "🔄 Updating project discovery index..."
	@uv run python project_discoverer.py --update-index 2>/dev/null || \
		echo "⚠️  Index update not available (check implementation)"

# Configuration management
show-config:
	@echo "🔧 Project Discoverer Configuration:"
	@echo "Config file: pd_config.yaml"
	@if [ -f pd_config.yaml ]; then \
		echo "✅ Config file exists"; \
		cat pd_config.yaml; \
	else \
		echo "❌ Config file not found"; \
		echo "💡 Copy pd_config.yaml.example to pd_config.yaml"; \
	fi

setup-config:
	@if [ ! -f pd_config.yaml ]; then \
		echo "📋 Setting up configuration..."; \
		cp pd_config.yaml.example pd_config.yaml; \
		echo "✅ Configuration file created!"; \
		echo "💡 Edit pd_config.yaml to customize search paths"; \
	else \
		echo "✅ Configuration file already exists"; \
	fi

edit-config:
	@if [ ! -f pd_config.yaml ]; then \
		make setup-config; \
	fi
	@echo "📝 Opening configuration file..."
	@$${EDITOR:-nano} pd_config.yaml

# Development helpers
dev-test:
	@echo "🧪 Running development tests..."
	@make find QUERY=test || echo "⚠️  No test projects found"
	@make find QUERY=calmmage || echo "⚠️  Main project not found"

# Quick searches for common terms
find-bots:
	@make find QUERY=bot

find-tools:
	@make find QUERY=tool

find-schedulers:
	@make find QUERY=scheduler

find-experiments:
	@make find QUERY=experiment

# Show usage stats
stats:
	@echo "📊 Project Discoverer Statistics:"
	@echo "Config file: $$([ -f pd_config.yaml ] && echo '✅ Present' || echo '❌ Missing')"
	@echo "Example config: $$([ -f pd_config.yaml.example ] && echo '✅ Present' || echo '❌ Missing')"
	@echo "Total scenarios: $$(ls -1 notes/scenarios/ 2>/dev/null | wc -l || echo 0)"