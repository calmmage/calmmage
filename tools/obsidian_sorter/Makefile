# Obsidian Sorter - Command shortcuts
# Run with: make <command>

# Default goal shows help
.DEFAULT_GOAL := help

# Configuration
CONFIG_PATH := config.yaml

# Individual cleanup commands
daily-cleanup: ## Clean up daily folder - move daily notes IN, non-daily OUT
	uv run python daily_simple.py cleanup-daily --config-path $(CONFIG_PATH)

daily-cleanup-dry: ## Dry run of daily cleanup
	uv run python daily_simple.py cleanup-daily --config-path $(CONFIG_PATH) --dry-run

daily-cleanup-yes: ## Daily cleanup with auto-confirm (no prompts)
	uv run python daily_simple.py cleanup-daily --config-path $(CONFIG_PATH) --yes

weekly-cleanup: ## Clean up weekly folder - move weekly notes IN, non-weekly OUT, rename old formats
	uv run python daily_simple.py cleanup-weekly --config-path $(CONFIG_PATH)

weekly-cleanup-dry: ## Dry run of weekly cleanup
	uv run python daily_simple.py cleanup-weekly --config-path $(CONFIG_PATH) --dry-run

weekly-cleanup-yes: ## Weekly cleanup with auto-confirm (no prompts)
	uv run python daily_simple.py cleanup-weekly --config-path $(CONFIG_PATH) --yes

auto-link: ## Auto-link files to daily notes based on edit/creation dates
	uv run python daily_simple.py auto-link --config-path $(CONFIG_PATH)

auto-link-dry: ## Dry run of auto-linking
	uv run python daily_simple.py auto-link --config-path $(CONFIG_PATH) --dry-run

auto-link-yes: ## Auto-linking with auto-confirm (no prompts)
	uv run python daily_simple.py auto-link --config-path $(CONFIG_PATH) --yes

generic-cleanup: ## Organize all configured note types - move files to correct typed folders
	uv run python generic_note_cleanup.py --config-path $(CONFIG_PATH)

generic-cleanup-dry: ## Dry run of generic cleanup
	uv run python generic_note_cleanup.py --config-path $(CONFIG_PATH) --dry-run

generic-cleanup-yes: ## Generic cleanup with auto-confirm (no prompts)
	uv run python generic_note_cleanup.py --config-path $(CONFIG_PATH) --yes

# Combined operations
run-all: ## Run all operations: daily + weekly + auto-linking
	uv run python daily_simple.py run-all --config-path $(CONFIG_PATH)

run-all-dry: ## Dry run of all operations
	uv run python daily_simple.py run-all --config-path $(CONFIG_PATH) --dry-run

run-all-yes: ## All operations with auto-confirm (no prompts)
	uv run python daily_simple.py run-all --config-path $(CONFIG_PATH) --yes

full-cleanup: ## Complete cleanup: run-all + generic cleanup
	make run-all-yes
	make generic-cleanup-yes

full-cleanup-dry: ## Dry run of complete cleanup
	make run-all-dry
	make generic-cleanup-dry

# Scheduled job scripts (for automation)
scheduled-daily: ## Run daily cleanup as scheduled job
	uv run python scripts/scheduled_tasks/obsidian_daily_cleanup.py

scheduled-weekly: ## Run weekly cleanup as scheduled job
	uv run python scripts/scheduled_tasks/obsidian_weekly_cleanup.py

scheduled-auto-link: ## Run auto-linking as scheduled job
	uv run python scripts/scheduled_tasks/obsidian_auto_linking.py

scheduled-generic: ## Run generic cleanup as scheduled job
	uv run python scripts/scheduled_tasks/obsidian_generic_cleanup.py

scheduled-full: ## Run full cleanup as scheduled job
	uv run python scripts/scheduled_tasks/obsidian_full_cleanup.py

# Utility commands
help: ## Show this help message
	@echo 'Available commands:'
	@echo ''
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ''
	@echo 'Usage examples:'
	@echo '  make daily-cleanup-dry   # Preview daily cleanup actions'
	@echo '  make auto-link           # Run auto-linking with confirmation'
	@echo '  make full-cleanup-yes    # Run complete cleanup without prompts'
	@echo '  make scheduled-full      # Run as scheduled job (for automation)'

.PHONY: daily-cleanup daily-cleanup-dry daily-cleanup-yes weekly-cleanup weekly-cleanup-dry weekly-cleanup-yes auto-link auto-link-dry auto-link-yes generic-cleanup generic-cleanup-dry generic-cleanup-yes run-all run-all-dry run-all-yes full-cleanup full-cleanup-dry scheduled-daily scheduled-weekly scheduled-auto-link scheduled-generic scheduled-full help