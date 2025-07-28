# Cronicle Scheduler Tool - Component 1
# Manages jobs via Cronicle API and provides generic job executor plugin

.PHONY: help install test create run list delete status setup-plugin

PYTHON := python3
CLI_DIR := cli
PLUGIN_DIR := plugin

# Default help
help:
	@echo "🕒 Cronicle Scheduler Tool"
	@echo ""
	@echo "Setup:"
	@echo "  make setup-plugin   - Setup Cronicle plugin"
	@echo "  make show-plugin-id - Show current plugin ID"
	@echo "  make set-plugin-id ID=your_id - Set plugin ID manually"
	@echo ""
	@echo "Job Management:"
	@echo "  make list           - List all Cronicle jobs (clean view)"
	@echo "  make list-full      - List all jobs with ID and target columns"
	@echo "  make list-enabled   - List only enabled jobs"
	@echo "  make create NAME='Job Name' JOB=/path/to/script.py - Create new job"
	@echo "  make run ID=event_id - Run job immediately"
	@echo "  make delete ID=event_id - Delete job"
	@echo "  make status ID=job_id - Check job status"
	@echo ""
	@echo "Advanced Creation:"
	@echo "  make create-scheduled NAME='Daily Job' JOB=/path/to/script.py HOURS=9 MINUTES=0"
	@echo "  make create-with-env NAME='Job' JOB=/path/to/script.py ENV=/path/to/.env"
	@echo ""
	@echo "Testing & Development:"
	@echo "  make test           - Test Cronicle connection"
	@echo "  make test-plugin    - Test job executor plugin"
	@echo ""
	@echo "Environment Setup:"
	@echo "  export CRONICLE_URL=http://localhost:3012"
	@echo "  export CRONICLE_API_KEY=your_api_key"

# Check environment variables
check-env:
	@if [ -z "$$CRONICLE_URL" ]; then \
		echo "❌ Error: CRONICLE_URL environment variable not set"; \
		echo "   Example: export CRONICLE_URL=http://localhost:3012"; \
		exit 1; \
	fi
	@if [ -z "$$CRONICLE_API_KEY" ]; then \
		echo "❌ Error: CRONICLE_API_KEY environment variable not set"; \
		echo "   Get this from your Cronicle web interface"; \
		exit 1; \
	fi

# Job Management Commands
list: check-env
	@uv run typer $(CLI_DIR)/cronicle_manager.py run list

list-full: check-env
	@uv run typer $(CLI_DIR)/cronicle_manager.py run list --full

list-enabled: check-env
	@uv run typer $(CLI_DIR)/cronicle_manager.py run list --exclude-disabled

create: check-env
	@if [ -z "$(NAME)" ] || [ -z "$(JOB)" ]; then \
		echo "❌ Error: NAME and JOB parameters required"; \
		echo "   Usage: make create NAME='Job Title' JOB=/path/to/script.py"; \
		exit 1; \
	fi
	@uv run typer $(CLI_DIR)/cronicle_manager.py run create "$(NAME)" "$(JOB)"

create-scheduled: check-env
	@if [ -z "$(NAME)" ] || [ -z "$(JOB)" ]; then \
		echo "❌ Error: NAME and JOB parameters required"; \
		exit 1; \
	fi
	@ARGS="$(NAME)" "$(JOB)"; \
	if [ -n "$(HOURS)" ]; then ARGS="$$ARGS --hours $(HOURS)"; fi; \
	if [ -n "$(MINUTES)" ]; then ARGS="$$ARGS --minutes $(MINUTES)"; fi; \
	if [ -n "$(WEEKDAYS)" ]; then ARGS="$$ARGS --weekdays $(WEEKDAYS)"; fi; \
	uv run typer $(CLI_DIR)/cronicle_manager.py run create $$ARGS

create-with-env: check-env
	@if [ -z "$(NAME)" ] || [ -z "$(JOB)" ]; then \
		echo "❌ Error: NAME and JOB parameters required"; \
		exit 1; \
	fi
	@ARGS="$(NAME)" "$(JOB)"; \
	if [ -n "$(ENV)" ]; then ARGS="$$ARGS --env-file $(ENV)"; fi; \
	if [ -n "$(KWARGS)" ]; then ARGS="$$ARGS --kwargs '$(KWARGS)'"; fi; \
	uv run typer $(CLI_DIR)/cronicle_manager.py run create $$ARGS

run: check-env
	@if [ -z "$(ID)" ]; then \
		echo "❌ Error: ID parameter required"; \
		echo "   Usage: make run ID=event_id"; \
		exit 1; \
	fi
	@uv run typer $(CLI_DIR)/cronicle_manager.py run run $(ID)

delete: check-env
	@if [ -z "$(ID)" ]; then \
		echo "❌ Error: ID parameter required"; \
		echo "   Usage: make delete ID=event_id"; \
		exit 1; \
	fi
	@uv run typer $(CLI_DIR)/cronicle_manager.py run delete $(ID)

status: check-env
	@if [ -z "$(ID)" ]; then \
		echo "❌ Error: ID parameter required"; \
		echo "   Usage: make status ID=job_id"; \
		exit 1; \
	fi
	@uv run typer $(CLI_DIR)/cronicle_manager.py run status $(ID)

# Testing
test: check-env
	@echo "🔍 Testing Cronicle connection..."
	@uv run typer $(CLI_DIR)/cronicle_manager.py run list > /dev/null && \
		echo "✅ Cronicle connection successful!" || \
		echo "❌ Cronicle connection failed!"

test-plugin:
	@echo "🧪 Testing job executor plugin..."
	@echo "Testing with simple Python script..."
	@echo 'print("Hello from test job!")' > /tmp/test_job.py
	@uv run python $(PLUGIN_DIR)/job_executor.py --executable /tmp/test_job.py
	@rm -f /tmp/test_job.py
	@echo "✅ Plugin test completed!"

# Plugin setup (for Cronicle admin)
setup-plugin:
	@echo "🔧 Setting up Cronicle plugin..."
	@echo "📋 Plugin configuration file: $(PLUGIN_DIR)/plugin_config.pixl"
	@echo "🔍 Job executor: $(PLUGIN_DIR)/job_executor.py"
	@echo ""
	@echo "📖 Manual setup required:"
	@echo "1. Copy plugin_config.pixl contents to Cronicle web interface (Admin > Plugins > Add Plugin)"
	@echo "2. Update binary path in plugin config to: $$(pwd)/$(PLUGIN_DIR)/job_executor.py"
	@echo "3. Install plugin and note the Plugin ID"
	@echo "4. Plugin ID will be prompted on first use and saved to .plugin_id file"
	@echo ""
	@echo "Current plugin binary path should be:"
	@echo "   $$(pwd)/$(PLUGIN_DIR)/job_executor.py"
	@echo ""
	@if [ -f .plugin_id ]; then \
		echo "✅ Plugin ID file exists: $$(cat .plugin_id)"; \
	else \
		echo "⚠️  Plugin ID file not found - will be created on first use"; \
	fi

# Development helpers
dev-test: test-plugin test

# Plugin ID management
show-plugin-id:
	@if [ -f .plugin_id ]; then \
		echo "✅ Current plugin ID: $$(cat .plugin_id)"; \
	else \
		echo "❌ Plugin ID not set. Run a create command to set it interactively."; \
	fi

set-plugin-id:
	@if [ -z "$(ID)" ]; then \
		echo "❌ Error: ID parameter required"; \
		echo "   Usage: make set-plugin-id ID=your_plugin_id"; \
		exit 1; \
	fi
	@echo "$(ID)" > .plugin_id
	@echo "✅ Plugin ID set to: $(ID)"

# Show plugin info
plugin-info:
	@echo "🔧 Cronicle Plugin Information:"
	@echo "Plugin config: $(PLUGIN_DIR)/plugin_config.pixl"
	@echo "Job executor: $(PLUGIN_DIR)/job_executor.py"
	@echo "Binary path for Cronicle: $$(pwd)/$(PLUGIN_DIR)/job_executor.py"
	@echo "Plugin ID: $$([ -f .plugin_id ] && cat .plugin_id || echo 'Not set')"
	@echo ""
	@echo "Supported parameters:"
	@echo "  - executable: Path to script/binary to run"
	@echo "  - env_file: Path to .env file (optional)"  
	@echo "  - kwargs: JSON string of arguments (optional)"

# Examples
examples:
	@echo "📚 Usage Examples:"
	@echo ""
	@echo "# Create simple job"
	@echo "make create NAME='Hello World' JOB=/path/to/hello.py"
	@echo ""
	@echo "# Create scheduled job (daily at 9 AM)"
	@echo "make create-scheduled NAME='Daily Backup' JOB=/path/to/backup.py HOURS=9 MINUTES=0"
	@echo ""
	@echo "# Create job with environment file"
	@echo "make create-with-env NAME='DB Job' JOB=/path/to/db_job.py ENV=/path/to/.env"
	@echo ""
	@echo "# Create job with custom arguments"
	@echo "make create-with-env NAME='Custom Job' JOB=/path/to/job.py KWARGS='{\"debug\": true}'"