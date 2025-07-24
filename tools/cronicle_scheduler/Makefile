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
	@echo "Setup & Installation:"
	@echo "  make install        - Install Python dependencies"
	@echo "  make setup-plugin   - Setup Cronicle plugin"
	@echo ""
	@echo "Job Management:"
	@echo "  make list           - List all Cronicle jobs"
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

# Installation
install:
	@echo "📦 Installing Cronicle Scheduler dependencies..."
	@$(PYTHON) -m pip install typer rich requests python-dotenv

# Job Management Commands
list: check-env
	@$(PYTHON) $(CLI_DIR)/cronicle_manager.py list

create: check-env
	@if [ -z "$(NAME)" ] || [ -z "$(JOB)" ]; then \
		echo "❌ Error: NAME and JOB parameters required"; \
		echo "   Usage: make create NAME='Job Title' JOB=/path/to/script.py"; \
		exit 1; \
	fi
	@$(PYTHON) $(CLI_DIR)/cronicle_manager.py create "$(NAME)" "$(JOB)"

create-scheduled: check-env
	@if [ -z "$(NAME)" ] || [ -z "$(JOB)" ]; then \
		echo "❌ Error: NAME and JOB parameters required"; \
		exit 1; \
	fi
	@ARGS="$(NAME)" "$(JOB)"; \
	if [ -n "$(HOURS)" ]; then ARGS="$$ARGS --hours $(HOURS)"; fi; \
	if [ -n "$(MINUTES)" ]; then ARGS="$$ARGS --minutes $(MINUTES)"; fi; \
	if [ -n "$(WEEKDAYS)" ]; then ARGS="$$ARGS --weekdays $(WEEKDAYS)"; fi; \
	$(PYTHON) $(CLI_DIR)/cronicle_manager.py create $$ARGS

create-with-env: check-env
	@if [ -z "$(NAME)" ] || [ -z "$(JOB)" ]; then \
		echo "❌ Error: NAME and JOB parameters required"; \
		exit 1; \
	fi
	@ARGS="$(NAME)" "$(JOB)"; \
	if [ -n "$(ENV)" ]; then ARGS="$$ARGS --env-file $(ENV)"; fi; \
	if [ -n "$(KWARGS)" ]; then ARGS="$$ARGS --kwargs '$(KWARGS)'"; fi; \
	$(PYTHON) $(CLI_DIR)/cronicle_manager.py create $$ARGS

run: check-env
	@if [ -z "$(ID)" ]; then \
		echo "❌ Error: ID parameter required"; \
		echo "   Usage: make run ID=event_id"; \
		exit 1; \
	fi
	@$(PYTHON) $(CLI_DIR)/cronicle_manager.py run $(ID)

delete: check-env
	@if [ -z "$(ID)" ]; then \
		echo "❌ Error: ID parameter required"; \
		echo "   Usage: make delete ID=event_id"; \
		exit 1; \
	fi
	@$(PYTHON) $(CLI_DIR)/cronicle_manager.py delete $(ID)

status: check-env
	@if [ -z "$(ID)" ]; then \
		echo "❌ Error: ID parameter required"; \
		echo "   Usage: make status ID=job_id"; \
		exit 1; \
	fi
	@$(PYTHON) $(CLI_DIR)/cronicle_manager.py status $(ID)

# Testing
test: check-env
	@echo "🔍 Testing Cronicle connection..."
	@$(PYTHON) $(CLI_DIR)/cronicle_manager.py list > /dev/null && \
		echo "✅ Cronicle connection successful!" || \
		echo "❌ Cronicle connection failed!"

test-plugin:
	@echo "🧪 Testing job executor plugin..."
	@echo "Testing with simple Python script..."
	@echo 'print("Hello from test job!")' > /tmp/test_job.py
	@$(PYTHON) $(PLUGIN_DIR)/job_executor.py --executable /tmp/test_job.py
	@rm -f /tmp/test_job.py
	@echo "✅ Plugin test completed!"

# Plugin setup (for Cronicle admin)
setup-plugin:
	@echo "🔧 Setting up Cronicle plugin..."
	@echo "📋 Plugin configuration file: $(PLUGIN_DIR)/plugin_config.pixl"
	@echo "🔍 Job executor: $(PLUGIN_DIR)/job_executor.py"
	@echo ""
	@echo "📖 Manual setup required:"
	@echo "1. Copy plugin_config.pixl contents to Cronicle web interface"
	@echo "2. Update binary path in plugin config to: $$(pwd)/$(PLUGIN_DIR)/job_executor.py"
	@echo "3. Install plugin in Cronicle admin panel"
	@echo ""
	@echo "Current plugin binary path should be:"
	@echo "   $$(pwd)/$(PLUGIN_DIR)/job_executor.py"

# Development helpers
dev-test: test-plugin test

# Show plugin info
plugin-info:
	@echo "🔧 Cronicle Plugin Information:"
	@echo "Plugin config: $(PLUGIN_DIR)/plugin_config.pixl"
	@echo "Job executor: $(PLUGIN_DIR)/job_executor.py"
	@echo "Binary path for Cronicle: $$(pwd)/$(PLUGIN_DIR)/job_executor.py"
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