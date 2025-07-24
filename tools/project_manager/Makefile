# Project Manager Tool
# Manages project creation, organization, and development workflows

.PHONY: help install test new-project new-mini-project new-todo new-feature move-to-examples get-project

PYTHON := python3
CLI := pm_cli.py

help:
	@echo "📁 Project Manager Tool"
	@echo ""
	@echo "Setup:"
	@echo "  make install        - Install dependencies"
	@echo "  make test           - Test tool functionality"
	@echo ""
	@echo "Project Creation:"
	@echo "  make new-project NAME=project_name - Create new project in GitHub + experiments"
	@echo "  make new-mini-project NAME=mini_name - Create new mini-project in seasonal folder"
	@echo ""
	@echo "Project Development:"
	@echo "  make new-todo PROJECT=project_name - Create new todo file in project"
	@echo "  make new-feature PROJECT=project_name FEATURE=feature_name - Create feature directory"
	@echo "  make get-project PATH=/path/to/check - Get project directory for path"
	@echo ""
	@echo "File Management:"
	@echo "  make move-to-examples SOURCE=/path/to/file - Move file to examples destination"
	@echo ""
	@echo "Examples:"
	@echo "  make new-project NAME=my-awesome-app"
	@echo "  make new-mini-project NAME=quick-experiment"
	@echo "  make new-todo PROJECT=my-project"
	@echo "  make new-feature PROJECT=my-project FEATURE=user-auth"

install:
	@echo "📦 Project Manager dependencies managed by uv"
	@echo "✅ No separate installation needed - use 'uv run' commands"

test:
	@echo "🧪 Testing Project Manager..."
	@uv run typer $(CLI) run --help > /dev/null && echo "✅ CLI working!" || echo "❌ CLI failed!"

# Project Creation Commands
new-project:
	@if [ -z "$(NAME)" ]; then \
		echo "❌ Error: NAME parameter required"; \
		echo "   Usage: make new-project NAME=project_name"; \
		exit 1; \
	fi
	@echo "🆕 Creating new project: $(NAME)"
	@uv run typer $(CLI) run new-project $(NAME)

new-mini-project:
	@if [ -z "$(NAME)" ]; then \
		echo "❌ Error: NAME parameter required"; \
		echo "   Usage: make new-mini-project NAME=mini_project_name"; \
		exit 1; \
	fi
	@echo "🆕 Creating new mini-project: $(NAME)"
	@uv run typer $(CLI) run new-mini-project $(NAME)

# Project Development Commands  
new-todo:
	@if [ -z "$(PROJECT)" ]; then \
		echo "❌ Error: PROJECT parameter required"; \
		echo "   Usage: make new-todo PROJECT=project_name"; \
		exit 1; \
	fi
	@echo "📝 Creating new todo for project: $(PROJECT)"
	@uv run typer $(CLI) run new-todo $(PROJECT)

new-feature:
	@if [ -z "$(PROJECT)" ] || [ -z "$(FEATURE)" ]; then \
		echo "❌ Error: PROJECT and FEATURE parameters required"; \
		echo "   Usage: make new-feature PROJECT=project_name FEATURE=feature_name"; \
		exit 1; \
	fi
	@echo "🚀 Creating new feature $(FEATURE) in project: $(PROJECT)"
	@uv run typer $(CLI) run new-feature $(FEATURE) --project-name $(PROJECT)

get-project:
	@if [ -z "$(PATH)" ]; then \
		echo "❌ Error: PATH parameter required"; \
		echo "   Usage: make get-project PATH=/path/to/check"; \
		exit 1; \
	fi
	@echo "🔍 Getting project directory for: $(PATH)"
	@uv run typer $(CLI) run get-project --path $(PATH)

# File Management Commands
move-to-examples:
	@if [ -z "$(SOURCE)" ]; then \
		echo "❌ Error: SOURCE parameter required"; \
		echo "   Usage: make move-to-examples SOURCE=/path/to/file"; \
		exit 1; \
	fi
	@echo "📦 Moving to examples: $(SOURCE)"
	@uv run typer $(CLI) run move-to-examples $(SOURCE)

# Development helpers
quick-project: 
	@echo "🚀 Creating quick test project..."
	@make new-mini-project NAME=test-$(shell date +%s)

# Configuration
show-config:
	@echo "🔧 Project Manager Configuration:"
	@echo "Config file: pm_config.yaml"
	@if [ -f pm_config.yaml ]; then \
		echo "✅ Config file exists"; \
		head -20 pm_config.yaml; \
	else \
		echo "❌ Config file not found"; \
		echo "💡 Copy pm_config.yaml.example to pm_config.yaml"; \
	fi

setup-config:
	@if [ ! -f pm_config.yaml ]; then \
		echo "📋 Setting up configuration..."; \
		cp pm_config.yaml.example pm_config.yaml; \
		echo "✅ Configuration file created!"; \
		echo "💡 Edit pm_config.yaml to customize settings"; \
	else \
		echo "✅ Configuration file already exists"; \
	fi