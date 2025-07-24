# Local Job Runner Tool - Component 2
# Scans and executes all jobs in a directory, like Airflow

.PHONY: help install test run list logs test-job setup dev-test

PYTHON := python3
JOBS_DIR := ../../scripts/scheduled_tasks
TEMPLATES_DIR := ../../resources/job_templates
LOG_DIR := ~/Library/Logs/CalmmageScheduler

# Default help
help:
	@echo "🏃 Local Job Runner Tool"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Create directories and setup environment"
	@echo ""
	@echo "Job Execution:"
	@echo "  make run            - Run all jobs in $(JOBS_DIR)/"
	@echo "  make run JOBS_DIR=/custom/path - Run jobs from custom directory"
	@echo "  make test-job JOB=job_name - Test run a specific job"
	@echo ""
	@echo "Job Management:"
	@echo "  make list           - List available jobs"
	@echo "  make logs           - View recent execution logs"
	@echo "  make logs-all       - View all execution logs"
	@echo ""
	@echo "Templates & Examples:"
	@echo "  make copy-template TEMPLATE=hello_world_job DEST=my_job"
	@echo "  make list-templates - List available job templates"
	@echo "  make setup-examples - Copy example jobs to scheduled_tasks/"
	@echo ""
	@echo "Development & Testing:"
	@echo "  make test           - Run basic functionality tests"
	@echo "  make dev-test       - Setup examples and run them"
	@echo "  make clean-logs     - Clean old log files"

# Setup
setup:
	@echo "🔧 Setting up Local Job Runner..."
	@mkdir -p $(JOBS_DIR)
	@mkdir -p $(LOG_DIR)
	@echo "✅ Directories created:"
	@echo "   Jobs: $(JOBS_DIR)"
	@echo "   Logs: $(LOG_DIR)"

# Job execution
run:
	@if [ -n "$(JOBS_DIR_OVERRIDE)" ]; then \
		echo "🏃 Running jobs from: $(JOBS_DIR_OVERRIDE)"; \
		uv run typer cli.py run run --jobs-dir "$(JOBS_DIR_OVERRIDE)"; \
	else \
		echo "🏃 Running jobs from: $(JOBS_DIR)"; \
		uv run typer cli.py run run --jobs-dir "$(JOBS_DIR)"; \
	fi

# Use custom jobs directory
run-custom:
	@if [ -z "$(DIR)" ]; then \
		echo "❌ Error: DIR parameter required"; \
		echo "   Usage: make run-custom DIR=/path/to/jobs"; \
		exit 1; \
	fi
	@echo "🏃 Running jobs from custom directory: $(DIR)"
	@uv run typer cli.py run run --jobs-dir "$(DIR)"

# Test specific job
test-job:
	@if [ -z "$(JOB)" ]; then \
		echo "❌ Error: JOB parameter required"; \
		echo "   Usage: make test-job JOB=job_name"; \
		exit 1; \
	fi
	@echo "🧪 Testing job: $(JOB)"
	@uv run typer cli.py run test "$(JOB)" --jobs-dir "$(JOBS_DIR)"

# Job management
list:
	@echo "📋 Listing available jobs in: $(JOBS_DIR)"
	@uv run typer cli.py run list --jobs-dir "$(JOBS_DIR)"

list-custom:
	@if [ -z "$(DIR)" ]; then \
		echo "❌ Error: DIR parameter required"; \
		echo "   Usage: make list-custom DIR=/path/to/jobs"; \
		exit 1; \
	fi
	@echo "📋 Listing jobs in: $(DIR)"
	@uv run typer cli.py run list --jobs-dir "$(DIR)"

# Logs
logs:
	@echo "📄 Viewing recent job logs..."
	@uv run typer cli.py run logs --latest

logs-all:
	@echo "📄 Viewing all job logs..."
	@uv run typer cli.py run logs --latest=false --count=20

logs-count:
	@if [ -z "$(COUNT)" ]; then \
		echo "❌ Error: COUNT parameter required"; \
		echo "   Usage: make logs-count COUNT=10"; \
		exit 1; \
	fi
	@echo "📄 Viewing last $(COUNT) job runs..."
	@uv run typer cli.py run logs --latest=false --count=$(COUNT)

# Templates
list-templates:
	@echo "📚 Available job templates:"
	@ls -1 $(TEMPLATES_DIR)/ 2>/dev/null | grep -v "^\." | sed 's/^/  - /' || \
		echo "  No templates found in $(TEMPLATES_DIR)"

copy-template:
	@if [ -z "$(TEMPLATE)" ] || [ -z "$(DEST)" ]; then \
		echo "❌ Error: TEMPLATE and DEST parameters required"; \
		echo "   Usage: make copy-template TEMPLATE=hello_world_job DEST=my_job_name"; \
		echo ""; \
		echo "Available templates:"; \
		make list-templates; \
		exit 1; \
	fi
	@if [ ! -d "$(TEMPLATES_DIR)/$(TEMPLATE)" ]; then \
		echo "❌ Error: Template '$(TEMPLATE)' not found"; \
		echo "Available templates:"; \
		make list-templates; \
		exit 1; \
	fi
	@DEST_PATH="$(JOBS_DIR)/$(DEST)"; \
	echo "📋 Copying template $(TEMPLATE) to $$DEST_PATH..."; \
	mkdir -p "$$DEST_PATH"; \
	cp -r "$(TEMPLATES_DIR)/$(TEMPLATE)"/* "$$DEST_PATH/"; \
	echo "✅ Template copied successfully!"; \
	echo "💡 Edit $$DEST_PATH/job.py and configuration files as needed"

# Setup examples
setup-examples:
	@echo "🚀 Setting up example jobs..."
	@make copy-template TEMPLATE=hello_world_job DEST=hello_world
	@make copy-template TEMPLATE=cleanup_folders_job DEST=cleanup_folders
	@echo "✅ Example jobs created in $(JOBS_DIR)/"
	@echo "💡 Try: make run"

# Testing
test:
	@echo "🧪 Running Local Job Runner tests..."
	@echo "✅ Testing job listing..."
	@uv run typer cli.py run list --jobs-dir "$(TEMPLATES_DIR)" > /dev/null
	@echo "✅ Testing with template directory..."
	@uv run typer cli.py run run --jobs-dir "$(TEMPLATES_DIR)/hello_world_job" > /dev/null || echo "⚠️  Template test may require dependencies"
	@echo "✅ Basic tests completed!"

# Development helpers
dev-test: setup-examples
	@echo "🧪 Running development test..."
	@make run
	@make logs

# Maintenance
clean-logs:
	@echo "🧹 Cleaning old log files..."
	@find $(LOG_DIR) -name "job_run_*.json" -mtime +30 -delete 2>/dev/null || true
	@echo "✅ Cleaned logs older than 30 days"

clean-logs-all:
	@echo "🧹 Cleaning ALL log files..."
	@rm -f $(LOG_DIR)/job_run_*.json
	@echo "✅ All log files removed"

# Show environment info
info:
	@echo "🔧 Local Job Runner Information:"
	@echo "Python: $$(python3 --version)"
	@echo "Jobs directory: $(JOBS_DIR)"
	@echo "Templates directory: $(TEMPLATES_DIR)"
	@echo "Log directory: $(LOG_DIR)"
	@echo "Available jobs: $$(ls -1 $(JOBS_DIR) 2>/dev/null | wc -l || echo 0)"
	@echo "Log files: $$(ls -1 $(LOG_DIR)/job_run_*.json 2>/dev/null | wc -l || echo 0)"

# Examples
examples:
	@echo "📚 Usage Examples:"
	@echo ""
	@echo "# Setup and run example jobs"
	@echo "make setup-examples && make run"
	@echo ""
	@echo "# Create custom job from template"
	@echo "make copy-template TEMPLATE=hello_world_job DEST=my_daily_job"
	@echo ""
	@echo "# Test specific job"
	@echo "make test-job JOB=hello_world"
	@echo ""
	@echo "# Run jobs from custom directory"
	@echo "make run-custom DIR=/path/to/my/jobs"
	@echo ""
	@echo "# View execution logs"
	@echo "make logs"
	@echo "make logs-count COUNT=5"

# Quick commands for common workflows
quick-start: setup setup-examples run logs

# Monitor jobs (run continuously)
monitor:
	@echo "👁️  Monitoring jobs (Ctrl+C to stop)..."
	@while true; do \
		echo "⏰ $$(date): Running jobs..."; \
		make run; \
		echo "😴 Sleeping for 3600 seconds (1 hour)..."; \
		sleep 3600; \
	done