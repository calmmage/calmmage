# Git Sync Tool Makefile
# Run commands with: make <target>

.PHONY: help sync-all sync-dry sync-verbose test-single install clean lint

help:  ## Show this help message
	@echo "Git Sync Tool - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Main sync commands
sync-all:  ## Sync all git repositories (quiet mode)
	uv run typer tools/git_sync_tool/cli.py run sync-all

sync-dry:  ## Dry run - show what would be synced without executing
	uv run typer tools/git_sync_tool/cli.py run sync-all --dry-run

sync-verbose:  ## Sync all repositories with detailed output
	uv run typer tools/git_sync_tool/cli.py run sync-all --verbose

sync-dry-verbose:  ## Dry run with verbose output
	uv run typer tools/git_sync_tool/cli.py run sync-all --dry-run --verbose

# Single repository sync
sync-single:  ## Sync a single repository (usage: make sync-single PATH=~/path/to/repo)
	@if [ -z "$(PATH_ARG)" ]; then \
		echo "Usage: make sync-single PATH_ARG=~/path/to/repo"; \
		exit 1; \
	fi
	uv run typer tools/git_sync_tool/cli.py run sync $(PATH_ARG)

# Advanced options
sync-no-backup:  ## Sync without creating backup branches (dangerous!)
	uv run typer tools/git_sync_tool/cli.py run sync-all --skip-backup

sync-custom-backup:  ## Sync with custom backup prefix (usage: make sync-custom-backup PREFIX=my-backup)
	@if [ -z "$(PREFIX)" ]; then \
		echo "Usage: make sync-custom-backup PREFIX=my-backup-name"; \
		exit 1; \
	fi
	uv run typer tools/git_sync_tool/cli.py run sync-all --backup-prefix $(PREFIX)

# Development and testing
test-tool:  ## Test the git sync tool on current directory
	uv run typer tools/git_sync_tool/cli.py run sync . --dry-run --verbose

lint:  ## Run linting on the tool code
	uv run ruff check tools/git_sync_tool/
	uv run mypy tools/git_sync_tool/ --ignore-missing-imports

format:  ## Format the tool code
	uv run ruff format tools/git_sync_tool/

# Automation job
run-job:  ## Run the automation job (used by local scheduler)
	uv run python scripts/local_jobs/git_sync_all.py

# Utilities
list-git-repos:  ## List all git repositories that would be processed
	@echo "Git repositories in ~/work/projects:"
	@find ~/work/projects -name ".git" -type d | sed 's|/.git||' | sed 's|.*/||' | sort

count-repos:  ## Count total repositories
	@echo "Total repositories: $$(find ~/work/projects ~/work/archive -name ".git" -type d | wc -l | tr -d ' ')"
	@echo "Active repositories (projects): $$(find ~/work/projects -name ".git" -type d | wc -l | tr -d ' ')"
	@echo "Archived repositories: $$(find ~/work/archive -name ".git" -type d | wc -l | tr -d ' ')"

clean:  ## Clean up any temporary files
	find tools/git_sync_tool -name "*.pyc" -delete
	find tools/git_sync_tool -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true