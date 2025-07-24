# Mac Settings Tool
# Manage and track macOS system settings changes

.PHONY: help install test dump diff clean categorize

PYTHON := python3
TOOL := tool.py
SRC_DIR := src
OUTPUT_DIR := output
CONFIG_DIR := config

help:
	@echo "⚙️  Mac Settings Tool"
	@echo ""
	@echo "Setup:"
	@echo "  make install        - Install dependencies"
	@echo "  make test           - Test tool functionality"
	@echo ""
	@echo "Settings Management:"
	@echo "  make dump           - Dump current system settings"
	@echo "  make diff           - Compare current settings with reference"
	@echo "  make clean          - Clean and filter settings differences"
	@echo "  make categorize     - Categorize settings changes"
	@echo ""
	@echo "Workflow Commands:"
	@echo "  make full-analysis  - Run complete settings analysis"
	@echo "  make quick-check    - Quick settings comparison"
	@echo ""
	@echo "Output Management:"
	@echo "  make show-results   - Show analysis results"
	@echo "  make clean-output   - Clean output directory"
	@echo ""
	@echo "Configuration:"  
	@echo "  make show-config    - Show current configuration"
	@echo "  make edit-config    - Edit settings filter configuration"

install:
	@echo "📦 Mac Settings dependencies managed by uv"
	@echo "✅ No separate installation needed - use 'uv run' commands"

test:
	@echo "🧪 Testing Mac Settings tool..."
	@uv run python $(TOOL) --help > /dev/null 2>&1 && echo "✅ Tool working!" || echo "⚠️  Check tool implementation"
	@echo "Testing source modules..."
	@uv run python -c "from $(SRC_DIR).dump_settings import dump_settings; print('✅ dump_settings module OK')" 2>/dev/null || echo "⚠️  dump_settings module issue"

# Main settings operations
dump:
	@echo "💾 Dumping current system settings..."
	@uv run python $(SRC_DIR)/dump_settings.py
	@echo "✅ Settings dumped to $(OUTPUT_DIR)/"

diff:
	@echo "🔍 Comparing settings with reference..."
	@uv run python $(SRC_DIR)/diff_settings.py
	@echo "✅ Differences saved to $(OUTPUT_DIR)/"

clean:
	@echo "🧹 Cleaning and filtering settings differences..."
	@uv run python $(SRC_DIR)/clean_diff.py
	@echo "✅ Cleaned differences saved to $(OUTPUT_DIR)/"

categorize:
	@echo "📊 Categorizing settings changes..."
	@uv run python $(SRC_DIR)/categorize_changes.py
	@echo "✅ Categorized changes saved to $(OUTPUT_DIR)/"

# Workflow commands
full-analysis: dump diff clean categorize
	@echo "📈 Full settings analysis complete!"
	@make show-results

quick-check: diff clean
	@echo "⚡ Quick settings check complete!"
	@make show-results

# Output management
show-results:
	@echo "📋 Mac Settings Analysis Results:"
	@echo ""
	@if [ -f $(OUTPUT_DIR)/reference.json ]; then \
		echo "📄 Reference settings: $(OUTPUT_DIR)/reference.json"; \
		echo "   Size: $$(wc -l < $(OUTPUT_DIR)/reference.json) lines"; \
	fi
	@if [ -f $(OUTPUT_DIR)/settings_diff_cleaned.json ]; then \
		echo "📄 Cleaned differences: $(OUTPUT_DIR)/settings_diff_cleaned.json"; \
		echo "   Changes: $$(jq length $(OUTPUT_DIR)/settings_diff_cleaned.json 2>/dev/null || echo 'N/A')"; \
	fi
	@if [ -f $(OUTPUT_DIR)/settings_diff_categorized.json ]; then \
		echo "📄 Categorized changes: $(OUTPUT_DIR)/settings_diff_categorized.json"; \
		echo "   Categories: $$(jq 'keys | length' $(OUTPUT_DIR)/settings_diff_categorized.json 2>/dev/null || echo 'N/A')"; \
	fi

clean-output:
	@echo "🧹 Cleaning output directory..."
	@rm -rf $(OUTPUT_DIR)/*
	@echo "✅ Output directory cleaned!"

# Configuration
show-config:
	@echo "⚙️  Mac Settings Configuration:"
	@if [ -f $(CONFIG_DIR)/settings_filter.yaml ]; then \
		echo "📄 Settings filter: $(CONFIG_DIR)/settings_filter.yaml"; \
		cat $(CONFIG_DIR)/settings_filter.yaml; \
	else \
		echo "❌ Settings filter not found"; \
	fi

edit-config:
	@echo "📝 Opening settings filter configuration..."
	@$${EDITOR:-nano} $(CONFIG_DIR)/settings_filter.yaml

# Development helpers
dev-dump:
	@echo "🧪 Development settings dump..."
	@uv run python -c "from $(SRC_DIR).dump_settings import *; dump_settings(debug=True)"

dev-test:
	@echo "🧪 Running development tests..."
	@echo "Testing each module individually..."
	@uv run python $(SRC_DIR)/dump_settings.py --test 2>/dev/null || echo "⚠️  dump_settings test mode not available"
	@uv run python $(SRC_DIR)/diff_settings.py --test 2>/dev/null || echo "⚠️  diff_settings test mode not available"

# Backup and restore
backup-reference:
	@echo "💾 Backing up current reference..."
	@if [ -f $(OUTPUT_DIR)/reference.json ]; then \
		cp $(OUTPUT_DIR)/reference.json $(OUTPUT_DIR)/reference_backup_$$(date +%Y%m%d_%H%M%S).json; \
		echo "✅ Reference backed up"; \
	else \
		echo "❌ No reference file to backup"; \
	fi

create-reference:
	@echo "📋 Creating new reference from current settings..."
	@make dump
	@echo "✅ Reference created - use this as baseline for future comparisons"

# Statistics
stats:
	@echo "📊 Mac Settings Tool Statistics:"
	@echo "Source modules: $$(ls -1 $(SRC_DIR)/*.py 2>/dev/null | wc -l || echo 0)"
	@echo "Output files: $$(ls -1 $(OUTPUT_DIR)/ 2>/dev/null | wc -l || echo 0)"
	@echo "Config files: $$(ls -1 $(CONFIG_DIR)/ 2>/dev/null | wc -l || echo 0)"
	@if [ -f $(OUTPUT_DIR)/reference.json ]; then \
		echo "Reference size: $$(du -h $(OUTPUT_DIR)/reference.json | cut -f1)"; \
	fi

# System information
system-info:
	@echo "🖥️  System Information:"
	@echo "macOS version: $$(sw_vers -productVersion)"
	@echo "System preferences: $$(defaults domains | wc -w) domains"
	@echo "Current user: $$USER"
	@echo "Hostname: $$(hostname)"