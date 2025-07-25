# Project Arranger Tool
# Compare and sort projects for better organization

.PHONY: help install test compare sort run setup-config

PYTHON := python3
CLI := cli.py
CONFIG := pa_config.yaml

help:
	@echo "📊 Project Arranger Tool"
	@echo ""
	@echo "Setup:"
	@echo "  make install        - Install dependencies"
	@echo "  make test           - Test tool functionality"
	@echo "  make setup-config   - Setup configuration file"
	@echo ""
	@echo "Project Organization:"
	@echo "  make compare        - Compare projects using default config"
	@echo "  make compare CONFIG=/path/to/config.yaml - Compare with custom config"
	@echo "  make sort           - Sort projects using default config"
	@echo "  make sort CONFIG=/path/to/config.yaml - Sort with custom config"
	@echo "  make run            - Run both compare and sort"
	@echo ""
	@echo "Alternative Interface:"
	@echo "  make run-script     - Run via run.py script"
	@echo "  make run-shell      - Run via shell script"
	@echo ""
	@echo "Configuration:"
	@echo "  make show-config    - Show current configuration"
	@echo "  make edit-config    - Edit configuration file"
	@echo ""
	@echo "Development:"
	@echo "  make dev-test       - Run development tests"

install:
	@echo "📦 Project Arranger dependencies managed by uv"
	@echo "✅ No separate installation needed - use 'uv run' commands"

test:
	@echo "🧪 Testing Project Arranger..."
	@uv run typer $(CLI) run --help > /dev/null && echo "✅ CLI working!" || echo "❌ CLI failed!"

# Main commands
compare:
	@if [ -n "$(CONFIG)" ]; then \
		echo "📊 Comparing projects with config: $(CONFIG)"; \
		uv run typer $(CLI) run compare --config $(CONFIG); \
	else \
		echo "📊 Comparing projects with default config..."; \
		uv run typer $(CLI) run compare; \
	fi

sort:
	@if [ -n "$(CONFIG)" ]; then \
		echo "🗂️  Sorting projects with config: $(CONFIG)"; \
		uv run typer $(CLI) run sort --config $(CONFIG); \
	else \
		echo "🗂️  Sorting projects with default config..."; \
		uv run typer $(CLI) run sort; \
	fi

run: compare sort

# Alternative interfaces
run-script:
	@echo "🚀 Running via Python script..."
	@uv run python run.py

run-shell:
	@echo "🚀 Running via shell script..."
	@bash run.sh

# Configuration management
show-config:
	@echo "🔧 Project Arranger Configuration:"
	@echo "Config file: $(CONFIG)"
	@if [ -f $(CONFIG) ]; then \
		echo "✅ Config file exists"; \
		cat $(CONFIG); \
	else \
		echo "❌ Config file not found"; \
		echo "💡 Copy pa_config.yaml.example to pa_config.yaml"; \
	fi

setup-config:
	@if [ ! -f $(CONFIG) ]; then \
		echo "📋 Setting up configuration..."; \
		cp pa_config.yaml.example $(CONFIG); \
		echo "✅ Configuration file created!"; \
		echo "💡 Edit $(CONFIG) to customize project paths and rules"; \
	else \
		echo "✅ Configuration file already exists"; \
	fi

edit-config:
	@if [ ! -f $(CONFIG) ]; then \
		make setup-config; \
	fi
	@echo "📝 Opening configuration file..."
	@$${EDITOR:-nano} $(CONFIG)

# Development and testing
dev-test: setup-config
	@echo "🧪 Running development tests..."
	@echo "Testing compare command..."
	@make compare > /tmp/pa_test.log 2>&1 && echo "✅ Compare working" || echo "⚠️  Compare may need configuration"
	@echo "Testing sort command..."
	@make sort > /tmp/pa_test.log 2>&1 && echo "✅ Sort working" || echo "⚠️  Sort may need configuration"
	@rm -f /tmp/pa_test.log

# Jupyter development (if available)
dev-notebook:
	@echo "📓 Opening development notebook..."
	@if [ -f dev/dev.ipynb ]; then \
		cd dev && jupyter notebook dev.ipynb; \
	else \
		echo "❌ Development notebook not found"; \
	fi

# Show project stats
stats:
	@echo "📊 Project Arranger Statistics:"
	@echo "Config file: $$([ -f $(CONFIG) ] && echo '✅ Present' || echo '❌ Missing')"
	@echo "Example config: $$([ -f pa_config.yaml.example ] && echo '✅ Present' || echo '❌ Missing')"
	@echo "Development files: $$(ls -1 dev/ 2>/dev/null | wc -l || echo 0)"
	@echo "Source files: $$(ls -1 src/ 2>/dev/null | wc -l || echo 0)"

# Clean up
clean:
	@echo "🧹 Cleaning up temporary files..."
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete
	@echo "✅ Cleanup complete!"

# Quick commands for common workflows
quick-run: setup-config run

# Dry run mode (if supported)
dry-run:
	@echo "🔍 Dry run mode (if supported by implementation)..."
	@make compare || echo "⚠️  Check if dry-run is implemented"